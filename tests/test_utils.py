"""Tests for utils"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import asyncio
import os
import tempfile

import pytest

from jupyter_core.utils import deprecation, ensure_async, ensure_dir_exists, run_sync


def test_ensure_dir_exists():
    with tempfile.TemporaryDirectory() as td:
        ensure_dir_exists(td)
        ensure_dir_exists(os.path.join(str(td), "foo"), 0o777)


def test_deprecation():
    with pytest.deprecated_call():
        deprecation("foo")


async def afunc():
    return "afunc"


def func():
    return "func"


sync_afunc = run_sync(afunc)


def test_run_sync():
    async def foo():
        return 1

    foo_sync = run_sync(foo)
    assert foo_sync() == 1
    assert foo_sync() == 1

    asyncio.set_event_loop(None)
    assert foo_sync() == 1

    asyncio.run(foo())


def test_ensure_async():
    async def main():
        assert await ensure_async(afunc()) == "afunc"
        assert await ensure_async(func()) == "func"

    asyncio.run(main())
