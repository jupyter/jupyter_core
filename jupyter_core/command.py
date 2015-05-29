"""The root `jupyter` command.

This does nothing other than dispatch to subcommands.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

import argparse
import json
import os
import sys

from . import paths
from .version import __version__

class JupyterParser(argparse.ArgumentParser):
    
    @property
    def epilog(self):
        """Add subcommands to epilog on request
        
        Avoids searching PATH for subcommands unless help output is requested.
        """
        return 'Available subcommands: %s' % ' '.join(list_subcommands())
    
    @epilog.setter
    def epilog(self, x):
        """Ignore epilog set in Parser.__init__"""
        pass


def jupyter_parser():
    parser = JupyterParser(
        description="Jupyter: Interactive Computing",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--version', action='version', version=__version__)
    group.add_argument('subcommand', type=str, nargs='?', help='the subcommand to launch')
    
    # p = group.add_group('paths')
    group.add_argument('--config-dir', action='store_true',
        help="show Jupyter config dir")
    group.add_argument('--data-dir', action='store_true',
        help="show Jupyter data dir")
    group.add_argument('--runtime-dir', action='store_true',
        help="show Jupyter runtime dir")
    group.add_argument('--paths', action='store_true',
        help="show all Jupyter paths. Add --json for machine-readable format.")
    parser.add_argument('--json', action='store_true',
        help="output paths as machine-readable json")
    
    return parser

def list_subcommands():
    """List all jupyter subcommands
    
    searches PATH for `jupyter-name`
    
    Returns a list of jupyter's subcommand names, without the `jupyter-` prefix.
    Nested children (e.g. jupyter-sub-subsub) are not included.
    """
    path = os.environ.get('PATH') or os.defpath
    subcommands = set()
    for d in path.split(os.pathsep):
        try:
            names = os.listdir(d)
        except OSError:
            continue
        for name in names:
            if name.startswith('jupyter-'):
                subcommands.add(name.split('-')[1])
    return subcommands

def main():
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        # Don't parse if a subcommand is given
        # Avoids argparse gobbling up args passed to subcommand, such as `-h`.
        subcommand = sys.argv[1]
    else:
        parser = jupyter_parser()
        args, opts = parser.parse_known_args()
        subcommand = args.subcommand
        if args.json and not args.paths:
            print("--json is only used with --paths", file=sys.stderr)
            sys.exit(1)
        if args.config_dir:
            print(paths.jupyter_config_dir())
            return
        if args.data_dir:
            print(paths.jupyter_data_dir())
            return
        if args.runtime_dir:
            print(paths.jupyter_runtime_dir())
            return
        if args.paths:
            data = {}
            data['runtime'] = [paths.jupyter_runtime_dir()]
            data['config'] = paths.jupyter_config_path()
            data['data'] = paths.jupyter_path()
            if args.json:
                print(json.dumps(data))
            else:
                for name in sorted(data):
                    path = data[name]
                    print('%s:' % name)
                    for p in path:
                        print('    ' + p)
            return
    
    if not subcommand:
        parser.print_usage(file=sys.stderr)
        print("subcommand is required", file=sys.stderr)
        sys.exit(1)
    
    command = 'jupyter-' + subcommand
    try:
        os.execvp(command, sys.argv[1:])
    except OSError:
        print("jupyter: %r is not a Jupyter command" % subcommand, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
