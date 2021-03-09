"""TODO: these should be merged back into test_paths.py when they settle down
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import importlib
from unittest.mock import patch, Mock

import entrypoints

import pytest

from jupyter_core.paths import (
    jupyter_path, jupyter_config_path,
    JUPYTER_CONFIG_PATH_ENTRY_POINT, JUPYTER_DATA_PATH_ENTRY_POINT,
)


def test_data_entry_point(data_path_entry_point, tmp_path):
    data_path = jupyter_path()
    path = str(tmp_path / "foo/share")
    assert path in data_path


def test_config_entry_point(config_path_entry_point, tmp_path):
    config_path = jupyter_config_path()
    path = str(tmp_path / "bar/etc")
    assert path in config_path


# there's a lot of duplication, as ugly path hacks get confused otheriwse
@pytest.fixture
def foo_entry_point_module(tmp_path):
    with _mock_modspec("foo", tmp_path):
        yield


@pytest.fixture
def data_path_entry_point(foo_entry_point_module):
    with _mock_entry_point(JUPYTER_DATA_PATH_ENTRY_POINT, "foo-config", "foo", "share"):
        yield


@pytest.fixture
def bar_entry_point_module(tmp_path):
    with _mock_modspec("bar", tmp_path):
        yield


@pytest.fixture
def config_path_entry_point(bar_entry_point_module):
    loader = _mock_entry_point(JUPYTER_CONFIG_PATH_ENTRY_POINT, "bar-config", "bar", "etc")
    with loader:
        yield


def _mock_modspec(name, tmp_path):
    mod = tmp_path / f"{name}/__init__.py"
    mod.parent.mkdir()
    mod.write_text('__version__ = "0.1.0"')
    spec = Mock()
    spec.origin = str(mod)
    return patch.object(importlib.util, 'find_spec', return_value=spec)


def _mock_entry_point(ep_group, ep_name, module_name, object_name):
    ep = Mock()
    ep.name = ep_name
    ep.module_name = module_name
    ep.object_name = object_name
    return patch.object(entrypoints, 'get_group_named', return_value={ep_name: ep})
