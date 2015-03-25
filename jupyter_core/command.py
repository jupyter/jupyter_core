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


def jupyter_parser():
    parser = argparse.ArgumentParser(
        description="Jupyter: Interactive Computing"
    )
    parser.add_argument('subcommand', type=str, help='The subcommand to launch')
    return parser


def main():
    parser = jupyter_parser()
    args, opts = parser.parse_known_args()
    subcommand = 'jupyter-{}'.format(args.subcommand)
    if which(subcommand):
        os.execvp(subcommand, sys.argv[1:])
    else:
        print("No such command: %s" % subcommand, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
