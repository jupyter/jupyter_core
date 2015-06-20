"""Migrating IPython < 4.0 to Jupyter

This *copies* configuration and resources to their new locations in Jupyter

Migrations:

- .ipython/
  - nbextensions -> JUPYTER_DATA_DIR/nbextensions
  - kernels ->  JUPYTER_DATA_DIR/kernels
- .ipython/profile_default/
  - static/custom -> .jupyter/custom
  - nbconfig -> .jupyter/nbconfig
  - security/
    - notebook_secret, notebook_cookie_secret, nbsignatures.db -> JUPYTER_DATA_DIR
  - ipython_{notebook,nbconvert,qtconsole}_config.py -> .jupyter/jupyter_{name}_config.py


"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import re
import shutil
from datetime import datetime

from traitlets.config import PyFileConfigLoader, JSONFileConfigLoader

from ipython_genutils.path import ensure_dir_exists
try:
    from IPython.paths import get_ipython_dir, locate_profile
except ImportError:
    # IPython < 4
    from IPython.utils.path import get_ipython_dir, locate_profile

from .paths import jupyter_config_dir, jupyter_data_dir
from .application import JupyterApp

pjoin = os.path.join

migrations = {
    pjoin('{ipython_dir}', 'nbextensions'): pjoin('{jupyter_data}', 'nbextensions'),
    pjoin('{ipython_dir}', 'kernels'): pjoin('{jupyter_data}', 'kernels'),
    pjoin('{profile}', 'nbconfig'): pjoin('{jupyter_config}', 'nbconfig'),
}

custom_src_t = pjoin('{profile}', 'static', 'custom')
custom_dst_t = pjoin('{jupyter_config}', 'custom')

for security_file in ('notebook_secret', 'notebook_cookie_secret', 'nbsignatures.db'):
    src = pjoin('{profile}', 'security', security_file)
    dst = pjoin('{jupyter_data}', security_file)
    migrations[src] = dst

config_migrations = ['notebook', 'nbconvert', 'qtconsole']

regex = re.compile

config_substitutions = {
    regex(r'\bIPythonQtConsoleApp\b'): 'JupyterQtConsoleApp',
    regex(r'\bIPython\.html\b'): 'notebook',
    regex(r'\bIPython\.nbconvert\b'): 'nbconvert',
}

def migrate_dir(src, dst):
    """Migrate a directory from src to dst"""
    if not os.listdir(src):
        print("No files in %s" % src)
        return False
    if os.path.exists(dst):
        if os.listdir(dst):
            # already exists, non-empty
            print("%s already exists" % dst)
            return False
        else:
            os.rmdir(dst)
    print("Copying %s -> %s" % (src, dst))
    ensure_dir_exists(os.path.dirname(dst))
    shutil.copytree(src, dst, symlinks=True)
    return True


def migrate_file(src, dst, substitutions=None):
    """Migrate a single file from src to dst
    
    substitutions is an optional dict of {regex: replacement} for performing replacements on the file.
    """
    if os.path.exists(dst):
        # already exists
        print("%s already exists" % dst)
        return False
    print("Copying %s -> %s" % (src, dst))
    ensure_dir_exists(os.path.dirname(dst))
    shutil.copy(src, dst)
    if substitutions:
        with open(dst) as f:
            text = f.read()
        for pat, replacement in substitutions.items():
            text = pat.sub(replacement, text)
        with open(dst, 'w') as f:
            f.write(text)
    return True


def migrate_one(src, dst):
    """Migrate one item
    
    dispatches to migrate_dir/_file
    """
    if os.path.isfile(src):
        return migrate_file(src, dst)
    elif os.path.isdir(src):
        return migrate_dir(src, dst)
    else:
        print("Nothing to migrate for %s" % src)
        return False


def migrate_static_custom(src, dst):
    """Migrate non-empty custom.js,css from src to dst
    
    src, dst are 'custom' directories containing custom.{js,css}
    """
    migrated = False
    
    custom_js = pjoin(src, 'custom.js')
    custom_css = pjoin(src, 'custom.css')
    # check if custom_js is empty:
    custom_js_empty = True
    with open(custom_js) as f:
        js = f.read().strip()
        for line in js.splitlines():
            if not (
                line.isspace()
                or line.strip().startswith(('/*', '*', '//'))
            ):
                custom_js_empty = False
                break
    
    with open(custom_css) as f:
        css = f.read().strip()
        custom_css_empty = css.startswith('/*') and css.endswith('*/')
    
    if custom_js_empty:
        print("Ignoring empty %s" % custom_js)
    if custom_css_empty:
        print("Ignoring empty %s" % custom_css)
    
    if custom_js_empty and custom_css_empty:
        # nothing to migrate
        return False
    ensure_dir_exists(dst)
    
    if not custom_js_empty or not custom_css_empty:
        ensure_dir_exists(dst)
    
    if not custom_js_empty:
        if migrate_file(custom_js, pjoin(dst, 'custom.js')):
            migrated = True
    if not custom_css_empty:
        if migrate_file(custom_css, pjoin(dst, 'custom.css')):
            migrated = True
    
    return migrated


def migrate_config(name, env):
    """Migrate a config file
    
    Includes substitutions for updated configurable names.
    """
    src_base = pjoin('{profile}', 'ipython_{name}_config').format(name=name, **env)
    dst_base = pjoin('{jupyter_config}', 'jupyter_{name}_config').format(name=name, **env)
    loaders = {
        '.py': PyFileConfigLoader,
        '.json': JSONFileConfigLoader,
    }
    migrated = []
    for ext in ('.py', '.json'):
        src = src_base + ext
        dst = dst_base + ext
        if os.path.exists(src):
            cfg = loaders[ext](src).load_config()
            if cfg:
                if migrate_file(src, dst, substitutions=config_substitutions):
                    migrated.append(src)
            else:
                # don't migrate empty config files
                print("Not migrating empty config file: %s" % src)
    return migrated


def migrate():
    """Migrate IPython configuration to Jupyter"""
    env = {
        'jupyter_data': jupyter_data_dir(),
        'jupyter_config': jupyter_config_dir(),
        'ipython_dir': get_ipython_dir(),
        'profile': os.path.join(get_ipython_dir(), 'profile_default'),
    }
    for src_t, dst_t in migrations.items():
        src = src_t.format(**env)
        dst = dst_t.format(**env)
        if os.path.exists(src):
            if migrate_one(src, dst):
                pass
    
    for name in config_migrations:
        migrate_config(name, env)
    
    custom_src = custom_src_t.format(**env)
    custom_dst = custom_dst_t.format(**env)
    
    if os.path.exists(custom_src):
        migrate_static_custom(custom_src, custom_dst)
    # write a marker to avoid re-running migration checks
    ensure_dir_exists(env['jupyter_config'])
    with open(os.path.join(env['jupyter_config'], 'migrated'), 'w') as f:
        f.write(datetime.now().isoformat())


class MigrateApp(JupyterApp):
    name = 'jupyter-migrate'
    description = """
    Migrate configuration and data from .ipython prior to 4.0 to Jupyter locations.
    
    This migrates:
    
    - config files in the default profile
    - kernels in ~/.ipython/kernels
    - notebook javascript extensions in ~/.ipython/extensions
    - custom.js/css to .jupyter/custom
    
    to their new Jupyter locations.
    
    All files are copied, not moved.
    If the destinations already exist, nothing will be done.
    """
    
    def start(self):
        migrate()


main = MigrateApp.launch_instance


if __name__ == '__main__':
    main()

