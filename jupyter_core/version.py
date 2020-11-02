# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from collections import namedtuple

VersionInfo = namedtuple('VersionInfo', [
    'major',
    'minor',
    'micro',
    'releaselevel',
    'serial',
    'development',
    'developmentserial'
])

version_info = VersionInfo(4, 6, 4, 'final', 0, development=True, developmentserial=0)

_specifier_ = {'alpha': 'a', 'beta': 'b', 'candidate': 'rc'}

_suffix_ = ''

if version_info.releaselevel != 'final':
    _suffix_ += f'{_specifier_[version_info.releaselevel]}{version_info.serial}'

if version_info.development:
    _suffix_ += f'.dev{version_info.developmentserial}'

__version__ = f'{version_info.major}.{version_info.minor}.{version_info.micro}{_suffix_}'
