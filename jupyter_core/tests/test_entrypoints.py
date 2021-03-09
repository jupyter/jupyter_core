"""TODO: these should be merged back into test_paths.py when they settle down
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from unittest.mock import patch, Mock
import importlib

import pytest
import entrypoints

from jupyter_core.paths import (
    jupyter_path, jupyter_config_path,
    # these would stay
    JUPYTER_CONFIG_PATH_ENTRY_POINT, JUPYTER_DATA_PATH_ENTRY_POINT,
    # these might stay
    importlib_metadata, importlib_resources,
    # these would go
    JUPYTER_ENTRY_POINT_FINDER, JUPYTER_ENTRY_POINT_STRATEGY,
    JUPYTER_ENTRY_POINT_TIMINGS
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
    with _mock_entry_point(JUPYTER_DATA_PATH_ENTRY_POINT, "foo-config", "foo", "DATA", "share"):
        yield


@pytest.fixture
def bar_entry_point_module(tmp_path):
    with _mock_modspec("bar", tmp_path):
        yield


@pytest.fixture
def config_path_entry_point(bar_entry_point_module):
    loader = _mock_entry_point(JUPYTER_CONFIG_PATH_ENTRY_POINT, "bar-config", "bar", "CONFIG", "etc")
    with loader:
        yield


def _mock_modspec(name, tmp_path):
    mod = tmp_path / f"{name}/__init__.py"
    mod.parent.mkdir()

    # if deriving the path from the entry_point spec, the module _can_ be empty
    mod.write_text("\n".join(
        []
        if JUPYTER_ENTRY_POINT_STRATEGY == "INSPECT" else
        ["DATA = 'share'", "CONFIG = 'etc'"]
    ))

    spec = Mock()
    spec.origin = str(mod)

    return patch.object(importlib.util, 'find_spec', return_value=spec)


def _mock_entry_point(ep_group, ep_name, module_name, object_name, return_value):
    ep = Mock(spec=['load'])
    ep.name = ep_name

    if JUPYTER_ENTRY_POINT_STRATEGY == "INSPECT":
        object_name = return_value

    if JUPYTER_ENTRY_POINT_FINDER == "importlib_metadata":
        ep.module = module_name
        ep.attr = return_value
        return patch.object(importlib_metadata, 'entry_points', return_value={ep_group: [ep]})
    elif JUPYTER_ENTRY_POINT_FINDER == "entrypoints":
        ep.load.return_value = return_value
        ep.module_name = module_name
        ep.object_name = object_name
        return patch.object(entrypoints, 'get_group_named', return_value={ep_name: ep})
    else:
        raise NotImplementedError(JUPYTER_ENTRY_POINT_FINDER)
