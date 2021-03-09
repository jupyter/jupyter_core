"""Path utility functions."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Derived from IPython.utils.path, which is
# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.


import os
import ast
import sys
import stat
import errno
import time
import pathlib
import tempfile
import warnings
import functools
import traceback
import importlib


from contextlib import contextmanager

# TODO: clean these up when the correct tools are chosen
import entrypoints
if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata

pjoin = os.path.join

# UF_HIDDEN is a stat flag not defined in the stat module.
# It is used by BSD to indicate hidden files.
UF_HIDDEN = getattr(stat, 'UF_HIDDEN', 32768)


# TODO: remove, once the correct strategy is decided
JUPYTER_ENTRY_POINT_FINDER = os.environ.get("JUPYTER_ENTRY_POINT_FINDER", "entrypoints")
JUPYTER_ENTRY_POINT_STRATEGY = os.environ.get("JUPYTER_ENTRY_POINT_STRATEGY", "PARSE_OR_LOAD")
JUPYTER_ENTRY_POINT_TIMINGS = os.environ.get("JUPYTER_ENTRY_POINT_TIMINGS")


# The group names for entry_points in pyproject.toml, setup.py and .cfg to
# provide discoverable paths
if JUPYTER_ENTRY_POINT_STRATEGY == "INSPECT":
    # The entry_point MUST be the name of a directory, consisting of only
    # letters, numbers, and underscores, adjacent to __init__.py
    # and will never be loaded.
    JUPYTER_DATA_PATH_ENTRY_POINT = "jupyter_data_resource"
    JUPYTER_CONFIG_PATH_ENTRY_POINT = "jupyter_config_resource"
else:
    # The entry_point MUST resolve single string literal POSIX path relative to the
    # entry_point's importable
    JUPYTER_DATA_PATH_ENTRY_POINT = "jupyter_data_path"
    JUPYTER_CONFIG_PATH_ENTRY_POINT = "jupyter_config_path"

# TODO: remove if not parsing
# from https://github.com/pypa/setuptools/blob/23ee037d56a6d8ab957882e1a041f67924ae04da/setuptools/config.py#L19
class StaticModule:
    """
    Attempt to load the module by the name
    """
    def __init__(self, name):
        spec = importlib.util.find_spec(name)

        with open(spec.origin) as strm:
            src = strm.read()
        module = ast.parse(src)
        vars(self).update(locals())
        del self.self
        # add a path
        self.__file__ = spec.origin

    def __getattr__(self, attr):
        try:
            return next(
                ast.literal_eval(statement.value)
                for statement in self.module.body
                if isinstance(statement, ast.Assign)
                for target in statement.targets
                if isinstance(target, ast.Name) and target.id == attr
            )
        except Exception as e:
            raise AttributeError(
                "{self.name} has no attribute {attr}".format(**locals())
            ) from e

# TODO: remove if not parsing
@functools.lru_cache(maxsize=1024)
def _load_static_module(module_name):
    return StaticModule(module_name)


def _get_ep_name_object(ep):
    if JUPYTER_ENTRY_POINT_FINDER == "importlib_metadata":
        return ep.module, ep.attr
    elif JUPYTER_ENTRY_POINT_FINDER == "entrypoints":
        return ep.module_name, ep.object_name
    else:
        raise NotImplementedError(JUPYTER_ENTRY_POINT_FINDER)


def _load_path_from_one_entry_point(ep):
    """ get the paths from the entry_point target by importing
    """
    path = ep.load()
    module_name, object_name = _get_ep_name_object(ep)

    spec = importlib.util.find_spec(module_name)
    module = importlib.util.module_from_spec(spec)
    origin = pathlib.Path(module.__file__).parent.resolve()
    return str(origin / path)


def _parse_path_from_one_entry_point(ep):
    """ get the paths from the AST of the entry_point target without importing
    """
    module_name, object_name = _get_ep_name_object(ep)
    static_mod = _load_static_module(module_name)
    path = getattr(static_mod, object_name)
    origin = pathlib.Path(static_mod.__file__).parent.resolve()
    return str(origin / path)


def _parse_or_load_path_from_one_entry_point(ep):
    """ first attempt static discovery of the entry_point target, fall back to import
    """
    return _parse_path_from_one_entry_point(ep) or _load_path_from_one_entry_point(ep)

def _inspect_path_from_one_entry_point(ep):
    """ use the entrypoint attribute name to discover the path without loading
    """
    module_name, object_name = _get_ep_name_object(ep)
    spec = importlib.util.find_spec(module_name)
    module = importlib.util.module_from_spec(spec)
    origin = pathlib.Path(module.__file__).parent.resolve()
    return str(origin / object_name)


if JUPYTER_ENTRY_POINT_STRATEGY == "PARSE_OR_LOAD":
    _get_path_from_one_entry_point = _parse_or_load_path_from_one_entry_point
elif JUPYTER_ENTRY_POINT_STRATEGY == "LOAD":
    _get_path_from_one_entry_point = _load_path_from_one_entry_point
elif JUPYTER_ENTRY_POINT_STRATEGY == "PARSE":
    _get_path_from_one_entry_point = _parse_path_from_one_entry_point
elif JUPYTER_ENTRY_POINT_STRATEGY == "INSPECT":
    _get_path_from_one_entry_point = _inspect_path_from_one_entry_point
else:
    raise NotImplementedError(JUPYTER_ENTRY_POINT_STRATEGY)


def _entry_point_paths(ep_group):
    start = time.time()

    if JUPYTER_ENTRY_POINT_FINDER == "importlib_metadata":
        group = [(ep.name, ep) for ep in importlib_metadata.entry_points().get(ep_group, [])]
    elif JUPYTER_ENTRY_POINT_FINDER == "entrypoints":
        group = entrypoints.get_group_named(ep_group).items()
    else:
        raise NotImplementedError(JUPYTER_ENTRY_POINT_FINDER)

    JUPYTER_ENTRY_POINT_TIMINGS and print(
        f"{1e3 * (time.time() - start):.2f}ms {ep_group} loaded with {JUPYTER_ENTRY_POINT_FINDER}"
    )
    paths = []

    for name, ep in reversed(sorted(group)):
        try:
            ep_start = time.time()
            paths.append(_get_path_from_one_entry_point(ep))
        except Exception:
            warnings.warn('Failed to load {} from entry_point "{}"\n{}'.format(
                ep_group,
                name,
                traceback.format_exc()
            ))
        finally:
            JUPYTER_ENTRY_POINT_TIMINGS and print(
                f"{1e3 * (time.time() - ep_start):.2f}ms\t{ep_group}\t{name}"
            )


    end = time.time()
    JUPYTER_ENTRY_POINT_TIMINGS and print(f"{1e3 * (end - start):.2f}ms {ep_group}\tTOTAL")
    return paths



def envset(name):
    """Return True if the given environment variable is set

    An environment variable is considered set if it is assigned to a value
    other than 'no', 'n', 'false', 'off', '0', or '0.0' (case insensitive)
    """
    return os.environ.get(name, 'no').lower() not in ['no', 'n', 'false', 'off', '0', '0.0']

def get_home_dir():
    """Get the real path of the home directory"""
    homedir = os.path.expanduser('~')
    # Next line will make things work even when /home/ is a symlink to
    # /usr/home as it is on FreeBSD, for example
    homedir = os.path.realpath(homedir)
    return homedir

_dtemps = {}
def _mkdtemp_once(name):
    """Make or reuse a temporary directory.

    If this is called with the same name in the same process, it will return
    the same directory.
    """
    try:
        return _dtemps[name]
    except KeyError:
        d = _dtemps[name] = tempfile.mkdtemp(prefix=name + '-')
        return d

def jupyter_config_dir():
    """Get the Jupyter config directory for this platform and user.

    Returns JUPYTER_CONFIG_DIR if defined, else ~/.jupyter
    """

    env = os.environ
    home_dir = get_home_dir()

    if env.get('JUPYTER_NO_CONFIG'):
        return _mkdtemp_once('jupyter-clean-cfg')

    if env.get('JUPYTER_CONFIG_DIR'):
        return env['JUPYTER_CONFIG_DIR']

    return pjoin(home_dir, '.jupyter')


def jupyter_data_dir():
    """Get the config directory for Jupyter data files for this platform and user.

    These are non-transient, non-configuration files.

    Returns JUPYTER_DATA_DIR if defined, else a platform-appropriate path.
    """
    env = os.environ

    if env.get('JUPYTER_DATA_DIR'):
        return env['JUPYTER_DATA_DIR']

    home = get_home_dir()

    if sys.platform == 'darwin':
        return os.path.join(home, 'Library', 'Jupyter')
    elif os.name == 'nt':
        appdata = os.environ.get('APPDATA', None)
        if appdata:
            return pjoin(appdata, 'jupyter')
        else:
            return pjoin(jupyter_config_dir(), 'data')
    else:
        # Linux, non-OS X Unix, AIX, etc.
        xdg = env.get("XDG_DATA_HOME", None)
        if not xdg:
            xdg = pjoin(home, '.local', 'share')
        return pjoin(xdg, 'jupyter')


def jupyter_runtime_dir():
    """Return the runtime dir for transient jupyter files.

    Returns JUPYTER_RUNTIME_DIR if defined.

    The default is now (data_dir)/runtime on all platforms;
    we no longer use XDG_RUNTIME_DIR after various problems.
    """
    env = os.environ

    if env.get('JUPYTER_RUNTIME_DIR'):
        return env['JUPYTER_RUNTIME_DIR']

    return pjoin(jupyter_data_dir(), 'runtime')


if os.name == 'nt':
    programdata = os.environ.get('PROGRAMDATA', None)
    if programdata:
        SYSTEM_JUPYTER_PATH = [pjoin(programdata, 'jupyter')]
    else:  # PROGRAMDATA is not defined by default on XP.
        SYSTEM_JUPYTER_PATH = [os.path.join(sys.prefix, 'share', 'jupyter')]
else:
    SYSTEM_JUPYTER_PATH = [
        "/usr/local/share/jupyter",
        "/usr/share/jupyter",
    ]

ENV_JUPYTER_PATH = [os.path.join(sys.prefix, 'share', 'jupyter')]


def jupyter_path(*subdirs):
    """Return a list of directories to search for data files

    JUPYTER_PATH environment variable has highest priority.

    If the JUPYTER_PREFER_ENV_PATH environment variable is set, the environment-level
    directories will have priority over user-level directories.

    If ``*subdirs`` are given, that subdirectory will be added to each element.

    Examples:

    >>> jupyter_path()
    ['~/.local/jupyter', '/usr/local/share/jupyter']
    >>> jupyter_path('kernels')
    ['~/.local/jupyter/kernels', '/usr/local/share/jupyter/kernels']
    """

    paths = []

    # highest priority is explicit environment variable
    if os.environ.get('JUPYTER_PATH'):
        paths.extend(
            p.rstrip(os.sep)
            for p in os.environ['JUPYTER_PATH'].split(os.pathsep)
        )

    # Next is environment or user, depending on the JUPYTER_PREFER_ENV_PATH flag
    user = jupyter_data_dir()
    env = [p for p in ENV_JUPYTER_PATH if p not in SYSTEM_JUPYTER_PATH]
    entry_points = [p for p in _entry_point_paths(JUPYTER_DATA_PATH_ENTRY_POINT) if p not in SYSTEM_JUPYTER_PATH]

    if envset('JUPYTER_PREFER_ENV_PATH'):
        paths.extend(env)
        paths.extend(entry_points)
        paths.append(user)
    else:
        paths.append(user)
        paths.extend(env)
        paths.extend(entry_points)

    # finally, system
    paths.extend(SYSTEM_JUPYTER_PATH)

    # add subdir, if requested
    if subdirs:
        paths = [ pjoin(p, *subdirs) for p in paths ]
    return paths


if os.name == 'nt':
    programdata = os.environ.get('PROGRAMDATA', None)
    if programdata:
        SYSTEM_CONFIG_PATH = [os.path.join(programdata, 'jupyter')]
    else:  # PROGRAMDATA is not defined by default on XP.
        SYSTEM_CONFIG_PATH = []
else:
    SYSTEM_CONFIG_PATH = [
        "/usr/local/etc/jupyter",
        "/etc/jupyter",
    ]

ENV_CONFIG_PATH = [os.path.join(sys.prefix, 'etc', 'jupyter')]


def jupyter_config_path():
    """Return the search path for Jupyter config files as a list.

    If the JUPYTER_PREFER_ENV_PATH environment variable is set, the environment-level
    directories will have priority over user-level directories.
    """
    if os.environ.get('JUPYTER_NO_CONFIG'):
        # jupyter_config_dir makes a blank config when JUPYTER_NO_CONFIG is set.
        return [jupyter_config_dir()]

    paths = []

    # highest priority is explicit environment variable
    if os.environ.get('JUPYTER_CONFIG_PATH'):
        paths.extend(
            p.rstrip(os.sep)
            for p in os.environ['JUPYTER_CONFIG_PATH'].split(os.pathsep)
        )

    # Next is environment or user, depending on the JUPYTER_PREFER_ENV_PATH flag
    user = jupyter_config_dir()
    env = [p for p in ENV_CONFIG_PATH if p not in SYSTEM_CONFIG_PATH]
    entry_points = [p for p in _entry_point_paths(JUPYTER_CONFIG_PATH_ENTRY_POINT) if p not in SYSTEM_CONFIG_PATH]

    if envset('JUPYTER_PREFER_ENV_PATH'):
        paths.extend(env)
        paths.extend(entry_points)
        paths.append(user)
    else:
        paths.append(user)
        paths.extend(env)
        paths.extend(entry_points)

    # Finally, system path
    paths.extend(SYSTEM_CONFIG_PATH)
    return paths


def exists(path):
    """Replacement for `os.path.exists` which works for host mapped volumes
    on Windows containers
    """
    try:
        os.lstat(path)
    except OSError:
        return False
    return True


def is_file_hidden_win(abs_path, stat_res=None):
    """Is a file hidden?

    This only checks the file itself; it should be called in combination with
    checking the directory containing the file.

    Use is_hidden() instead to check the file and its parent directories.

    Parameters
    ----------
    abs_path : unicode
        The absolute path to check.
    stat_res : os.stat_result, optional
        The result of calling stat() on abs_path. If not passed, this function
        will call stat() internally.
    """
    if os.path.basename(abs_path).startswith('.'):
        return True

    if stat_res is None:
        try:
            stat_res = os.stat(abs_path)
        except OSError as e:
            if e.errno == errno.ENOENT:
                return False
            raise

    if stat_res.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN:
        return True

    return False


def is_file_hidden_posix(abs_path, stat_res=None):
    """Is a file hidden?

    This only checks the file itself; it should be called in combination with
    checking the directory containing the file.

    Use is_hidden() instead to check the file and its parent directories.

    Parameters
    ----------
    abs_path : unicode
        The absolute path to check.
    stat_res : os.stat_result, optional
        The result of calling stat() on abs_path. If not passed, this function
        will call stat() internally.
    """
    if os.path.basename(abs_path).startswith('.'):
        return True

    if stat_res is None or stat.S_ISLNK(stat_res.st_mode):
        try:
            stat_res = os.stat(abs_path)
        except OSError as e:
            if e.errno == errno.ENOENT:
                return False
            raise

    # check that dirs can be listed
    if stat.S_ISDIR(stat_res.st_mode):
        # use x-access, not actual listing, in case of slow/large listings
        if not os.access(abs_path, os.X_OK | os.R_OK):
            return True

    # check UF_HIDDEN
    if getattr(stat_res, 'st_flags', 0) & UF_HIDDEN:
        return True

    return False


if sys.platform == 'win32':
    is_file_hidden = is_file_hidden_win
else:
    is_file_hidden = is_file_hidden_posix


def is_hidden(abs_path, abs_root=''):
    """Is a file hidden or contained in a hidden directory?

    This will start with the rightmost path element and work backwards to the
    given root to see if a path is hidden or in a hidden directory. Hidden is
    determined by either name starting with '.' or the UF_HIDDEN flag as
    reported by stat.

    If abs_path is the same directory as abs_root, it will be visible even if
    that is a hidden folder. This only checks the visibility of files
    and directories *within* abs_root.

    Parameters
    ----------
    abs_path : unicode
        The absolute path to check for hidden directories.
    abs_root : unicode
        The absolute path of the root directory in which hidden directories
        should be checked for.
    """
    if os.path.normpath(abs_path) == os.path.normpath(abs_root):
        return False

    if is_file_hidden(abs_path):
        return True

    if not abs_root:
        abs_root = abs_path.split(os.sep, 1)[0] + os.sep
    inside_root = abs_path[len(abs_root):]
    if any(part.startswith('.') for part in inside_root.split(os.sep)):
        return True

    # check UF_HIDDEN on any location up to root.
    # is_file_hidden() already checked the file, so start from its parent dir
    path = os.path.dirname(abs_path)
    while path and path.startswith(abs_root) and path != abs_root:
        if not exists(path):
            path = os.path.dirname(path)
            continue
        try:
            # may fail on Windows junctions
            st = os.lstat(path)
        except OSError:
            return True
        if getattr(st, 'st_flags', 0) & UF_HIDDEN:
            return True
        path = os.path.dirname(path)

    return False


def win32_restrict_file_to_user(fname):
    """Secure a windows file to read-only access for the user.
    Follows guidance from win32 library creator:
    http://timgolden.me.uk/python/win32_how_do_i/add-security-to-a-file.html

    This method should be executed against an already generated file which
    has no secrets written to it yet.

    Parameters
    ----------

    fname : unicode
        The path to the file to secure
    """
    import win32api
    import win32security
    import ntsecuritycon as con

    # everyone, _domain, _type = win32security.LookupAccountName("", "Everyone")
    admins = win32security.CreateWellKnownSid(win32security.WinBuiltinAdministratorsSid)
    user, _domain, _type = win32security.LookupAccountName("", win32api.GetUserNameEx(win32api.NameSamCompatible))

    sd = win32security.GetFileSecurity(fname, win32security.DACL_SECURITY_INFORMATION)

    dacl = win32security.ACL()
    # dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_ALL_ACCESS, everyone)
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE | con.DELETE, user)
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_ALL_ACCESS, admins)

    sd.SetSecurityDescriptorDacl(1, dacl, 0)
    win32security.SetFileSecurity(fname, win32security.DACL_SECURITY_INFORMATION, sd)


def get_file_mode(fname):
    """Retrieves the file mode corresponding to fname in a filesystem-tolerant manner.

    Parameters
    ----------

    fname : unicode
        The path to the file to get mode from

    """
    # Some filesystems (e.g., CIFS) auto-enable the execute bit on files.  As a result, we
    # should tolerate the execute bit on the file's owner when validating permissions - thus
    # the missing least significant bit on the third octal digit. In addition, we also tolerate
    # the sticky bit being set, so the lsb from the fourth octal digit is also removed.
    return stat.S_IMODE(os.stat(fname).st_mode) & 0o6677  # Use 4 octal digits since S_IMODE does the same


allow_insecure_writes = os.getenv('JUPYTER_ALLOW_INSECURE_WRITES', 'false').lower() in ('true', '1')


@contextmanager
def secure_write(fname, binary=False):
    """Opens a file in the most restricted pattern available for
    writing content. This limits the file mode to `0o0600` and yields
    the resulting opened filed handle.

    Parameters
    ----------

    fname : unicode
        The path to the file to write

    binary: boolean
        Indicates that the file is binary
    """
    mode = 'wb' if binary else 'w'
    open_flag = os.O_CREAT | os.O_WRONLY | os.O_TRUNC
    try:
        os.remove(fname)
    except (IOError, OSError):
        # Skip any issues with the file not existing
        pass

    if os.name == 'nt':
        if allow_insecure_writes:
            # Mounted file systems can have a number of failure modes inside this block.
            # For windows machines in insecure mode we simply skip this to avoid failures :/
            issue_insecure_write_warning()
        else:
            # Python on windows does not respect the group and public bits for chmod, so we need
            # to take additional steps to secure the contents.
            # Touch file pre-emptively to avoid editing permissions in open files in Windows
            fd = os.open(fname, open_flag, 0o0600)
            os.close(fd)
            open_flag = os.O_WRONLY | os.O_TRUNC
            win32_restrict_file_to_user(fname)

    with os.fdopen(os.open(fname, open_flag, 0o0600), mode) as f:
        if os.name != 'nt':
            # Enforce that the file got the requested permissions before writing
            file_mode = get_file_mode(fname)
            if 0o0600 != file_mode:
                if allow_insecure_writes:
                    issue_insecure_write_warning()
                else:
                    raise RuntimeError("Permissions assignment failed for secure file: '{file}'."
                        " Got '{permissions}' instead of '0o0600'."
                        .format(file=fname, permissions=oct(file_mode)))
        yield f


def issue_insecure_write_warning():
    def format_warning(msg, *args, **kwargs):
        return str(msg) + '\n'

    warnings.formatwarning = format_warning
    warnings.warn("WARNING: Insecure writes have been enabled via environment variable "
                  "'JUPYTER_ALLOW_INSECURE_WRITES'! If this is not intended, remove the "
                  "variable or set its value to 'False'.")
