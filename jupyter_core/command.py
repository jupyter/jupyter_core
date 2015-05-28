"""The root `jupyter` command.

This does nothing other than dispatch to subcommands.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

import argparse
import os
import sys

try:
    # py3
    from shutil import which
except ImportError:
    from .utils.shutil_which import which

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
        description="Jupyter: Interactive Computing"
    )
    parser.add_argument('subcommand', type=str, help='The subcommand to launch')
    return parser

def list_subcommands():
    """List all jupyter subcommands
    
    searches PATH for `jupyter-name`
    
    Returns a list of jupyter's subcommand names, without the `jupyter-` prefix.
    Nested children (e.g. jupyter-sub-subsub) are not included.
    """
    prefix = 'jupyter-'
    path = os.environ.get('PATH') or os.defpath
    subcommands = set()
    for d in path.split(os.pathsep):
        try:
            names = os.listdir(d)
        except OSError:
            continue
        for name in names:
            if name.startswith(prefix):
                subcommands.add(name[len(prefix):])
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
    
    command = 'jupyter-' + subcommand
    try:
        os.execvp(command, sys.argv[1:])
    except OSError:
        print("jupyter: %r is not a Jupyter command" % subcommand, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
