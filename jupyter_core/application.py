# encoding: utf-8
"""
A base Application class for Jupyter applications.

All Jupyter applications should inherit from this.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

import logging
import os
import sys

try:
    # py3
    from shutil import which
except ImportError:
    from .utils.shutil_which import which

from traitlets.config.application import Application, catch_config_error
from traitlets.config.loader import ConfigFileNotFound
from traitlets import Unicode, Bool

from ipython_genutils.path import ensure_dir_exists
from ipython_genutils import py3compat

from .paths import jupyter_config_dir, jupyter_data_dir, jupyter_runtime_dir


if os.name == 'nt':
    programdata = os.environ.get('PROGRAMDATA', None)
    if programdata:
        SYSTEM_CONFIG_DIRS = [os.path.join(programdata, 'jupyter')]
    else:  # PROGRAMDATA is not defined by default on XP.
        SYSTEM_CONFIG_DIRS = []
else:
    SYSTEM_CONFIG_DIRS = [
        "/usr/local/etc/jupyter",
        "/etc/jupyter",
    ]


# aliases and flags

base_aliases = {
    'log-level' : 'Application.log_level',
}

base_flags = {
    'debug': ({'Application' : {'log_level' : logging.DEBUG}},
            "set log level to logging.DEBUG (maximize logging output)"),
    'generate-config': ({'JupyterApp': {'generate_config': True}},
        "generate default config file"),
}

class JupyterApp(Application):
    """Base class for Jupyter applications"""
    name = 'jupyter' # override in subclasses
    description = "A Jupyter Application"
    
    aliases = base_aliases
    flags = base_flags
    
    config_dir = Unicode()
    
    def _config_dir_default(self):
        return jupyter_config_dir()
    
    @property
    def config_file_paths(self):
        return [py3compat.getcwd(), self.config_dir] + SYSTEM_CONFIG_DIRS
    
    data_dir = Unicode()
    
    def _data_dir_default(self):
        d = jupyter_data_dir()
        ensure_dir_exists(d, mode=0o700)
        return d
    
    runtime_dir = Unicode()
    
    def _runtime_dir_default(self):
        rd = jupyter_runtime_dir()
        ensure_dir_exists(rd, mode=0o700)
        return rd
    
    def _runtime_dir_changed(self, new):
        ensure_dir_exists(new, mode=0o700)
    
    generate_config = Bool(False)
    
    config_file_name = Unicode()
    def _config_file_name_default(self):
        if not self.name:
            return ''
        return self.name.replace('-','_') + u'_config.py'
    
    @property
    def config_files(self):
        return [self.config_file_name]
    
    def write_config_file(self):
        """Write our default config to a .py config file"""
        if os.path.exists(self.config_file) and not self.answer_yes:
            answer = ''
            def ask():
                prompt = "Overwrite %s with default config? [y/N]" % self.config_file
                try:
                    return input(prompt).lower() or 'n'
                except KeyboardInterrupt:
                    print('') # empty line
                    return 'n'
            answer = ask()
            while not answer.startswith(('y', 'n')):
                print("Please answer 'yes' or 'no'")
                answer = ask()
            if answer.startswith('n'):
                return
        
        config_text = self.generate_config_file()
        if isinstance(config_text, bytes):
            config_text = config_text.decode('utf8')
        print("Writing default config to: %s" % self.config_file)
        with open(self.config_file, mode='w') as f:
            f.write(config_text)
    
    def load_config_file(self, suppress_errors=True):
        """Load the config file.

        By default, errors in loading config are handled, and a warning
        printed on screen. For testing, the suppress_errors option is set
        to False, so errors will make tests fail.
        """
        self.log.debug("Searching %s for config files", self.config_file_paths)
        base_config = 'jupyter_config'
        self.log.debug("Attempting to load config file: %s" %
                       base_config)
        try:
            Application.load_config_file(
                self,
                base_config,
                path=self.config_file_paths
            )
        except ConfigFileNotFound:
            # ignore errors loading parent
            self.log.debug("Config file %s not found", base_config)
            pass
        
        for config_file_name in self.config_files:
            if not config_file_name or config_file_name == base_config:
                continue
            self.log.debug("Attempting to load config file: %s" %
                           self.config_file_name)
            try:
                Application.load_config_file(
                    self,
                    config_file_name,
                    path=self.config_file_paths
                )
            except ConfigFileNotFound:
                self.log.debug("Config file not found, skipping: %s", config_file_name)
            except:
                # For testing purposes.
                if not suppress_errors:
                    raise
                self.log.warn("Error loading config file: %s" %
                              self.config_file_name, exc_info=True)
    # subcommand-related
    def _find_subcommand(self, name):
        name = '{}-{}'.format(self.name, name)
        return which(name)
    
    @property
    def _dispatching(self):
        """Return whether we are dispatching to another command
        
        or running ourselves.
        """
        return bool(self.generate_config or self.subapp or self.subcommand)
    
    subcommand = Unicode()
    
    @catch_config_error
    def initialize(self, argv=None):
        # don't hook up crash handler before parsing command-line
        if argv is None:
            argv = sys.argv[1:]
        if argv:
            subc = self._find_subcommand(argv[0])
            if subc:
                self.argv = argv
                self.subcommand = subc
                return
        self.parse_command_line(argv)
        if self._dispatching:
            return
        self.load_config_file()
    
    
    def start(self):
        """Start the whole thing"""
        if self.subcommand:
            os.execv(self.subcommand, [self.subcommand] + self.argv[1:])
            return
        
        if self.subapp:
            self.subapp.start()
            return
        
        if self.generate_config:
            self.write_config_file()
            return

if __name__ == '__main__':
    JupyterApp.launch_instance()
