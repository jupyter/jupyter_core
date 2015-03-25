# encoding: utf-8
"""Path utility functions."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Derived from IPython.utils.path, which is
# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.


import os
import sys

pjoin = os.path.join


def get_home_dir():
    """Get the real path of the home directory"""
    homedir = os.path.expanduser('~')
    # Next line will make things work even when /home/ is a symlink to
    # /usr/home as it is on FreeBSD, for example
    homedir = os.path.realpath(homedir)
    return homedir


def jupyter_config_dir():
    """Get the Jupyter config directory for this platform and user.
    
    Returns JUPYTER_CONFIG_DIR if defined, else ~/.jupyter
    """

    env = os.environ
    home_dir = get_home_dir()

    if env.get('JUPYTER_CONFIG_DIR'):
        return env['JUPYTER_CONFIG_DIR']
    
    return pjoin(home_dir, '.jupyter')


def jupyter_data_dir():
    """Get the config directory for Jupyter data files.
    
    These are non-transient, non-configuration files.
    """
    env = os.environ
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
    
    Respects XDG_RUNTIME_HOME, falls back on data_dir/runtime otherwise.
    """
    env = os.environ

    if sys.platform == 'darwin':
        return pjoin(jupyter_data_dir(), 'runtime')
    elif os.name == 'nt':
        return pjoin(jupyter_data_dir(), 'runtime')
    else:
        # Linux, non-OS X Unix, AIX, etc.
        xdg = env.get("XDG_RUNTIME_HOME", None)
        if xdg:
            return pjoin(xdg, 'jupyter')
        return pjoin(jupyter_data_dir(), 'runtime')


