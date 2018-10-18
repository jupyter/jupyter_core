#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Juptyer Development Team.
# Distributed under the terms of the Modified BSD License.

#-----------------------------------------------------------------------------
# Minimal Python version sanity check (from IPython)
#-----------------------------------------------------------------------------
from __future__ import print_function

import os
import sys
from glob import glob

v = sys.version_info
if v[:2] < (2,7) or (v[:2] > (3,) and v[:2] < (3,3)):
    error = "ERROR: Jupyter requires Python version 2.7 or 3.3 or above."
    print(error, file=sys.stderr)
    sys.exit(1)

# At least we're on the python version we need, move on.

from distutils.core import setup

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))

# Get the current package version.
version_ns = {}
with open(pjoin(here, 'jupyter_core', 'version.py')) as f:
    exec(f.read(), {}, version_ns)


setup_args = dict(
    name                = 'jupyter_core',
    version             = version_ns['__version__'],
    packages            = ['jupyter_core',
                           'jupyter_core.utils',
                           'jupyter_core.tests'],
    py_modules          = ['jupyter'],
    scripts             = glob(pjoin('scripts', '*')),
    description         = "Jupyter core package. A base package on which Jupyter projects rely.",
    long_description    = """There is no reason to install this package on its own.""",
    author              = "Jupyter Development Team",
    author_email        = "jupyter@googlegroups.org",
    url                 = "https://jupyter.org",
    license             = "BSD",
    classifiers         = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)

if any(arg.startswith('bdist') for arg in sys.argv):
    import setuptools

setuptools_args = {}

setuptools_args['install_requires'] = [
    'traitlets',
]

setuptools_args['entry_points'] = {
    'console_scripts': [
        'jupyter = jupyter_core.command:main',
        'jupyter-migrate = jupyter_core.migrate:main',
        'jupyter-troubleshoot = jupyter_core.troubleshoot:main',
    ]
}

# setuptools requirements
if 'setuptools' in sys.modules:
    setup_args.update(setuptools_args)
    setup_args.pop('scripts', None)


if __name__ == '__main__':
    setup(**setup_args)
