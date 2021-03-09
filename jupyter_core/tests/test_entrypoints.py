"""TODO: these should be merged back into test_paths.py when they settle down
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from unittest.mock import patch, Mock
import importlib

import pytest
import entrypoints

from jupyter_core.paths import (
    jupyter_path, jupyter_config_path, JUPYTER_CONFIG_PATH_ENTRY_POINT,
    JUPYTER_DATA_PATH_ENTRY_POINT
)

@pytest.fixture
def foo_entry_point_module(tmp_path):
    mod = tmp_path / "foo/__init__.py"
    mod.parent.mkdir()
    mod.write_text("\n".join(["DATA = 'share'", "CONFIG = 'etc'"]))

    spec = Mock()
    spec.origin = str(mod)

    with patch.object(importlib.util, 'find_spec', return_value=spec):
        yield


@pytest.fixture
def data_path_entry_point(foo_entry_point_module):
    ep = Mock(spec=['load'])
    ep.name = JUPYTER_DATA_PATH_ENTRY_POINT
    ep.load.return_value = 'share'
    ep.module_name = "foo"
    ep.object_name = "DATA"

    with patch.object(entrypoints, 'get_group_named', return_value={'foo': ep}):
        yield ep


def test_data_entry_point(data_path_entry_point, tmp_path):
    data_path = jupyter_path()
    path = str(tmp_path / "foo/share")
    assert path in data_path


@pytest.fixture
def bar_entry_point_module(tmp_path):
    mod = tmp_path / "bar/__init__.py"
    mod.parent.mkdir()
    mod.write_text("\n".join(["DATA = 'share'", "CONFIG = 'etc'"]))

    spec = Mock()
    spec.origin = str(mod)

    with patch.object(importlib.util, 'find_spec', return_value=spec):
        yield


@pytest.fixture
def config_path_entry_point(bar_entry_point_module):
    ep = Mock(spec=['load'])
    ep.name = JUPYTER_CONFIG_PATH_ENTRY_POINT
    ep.load.return_value = 'etc'
    ep.module_name = "bar"
    ep.object_name = "CONFIG"

    with patch.object(entrypoints, 'get_group_named', return_value={'bar': ep}):
        yield ep


def test_config_entry_point(config_path_entry_point, tmp_path):
    config_path = jupyter_config_path()
    path = str(tmp_path / "bar/etc")
    assert path in config_path
