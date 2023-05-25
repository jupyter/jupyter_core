# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
# Note: copied from https://github.com/ipyflow/ipyflow/blob/8e4bc5cb8d4231b9b69f4f9dce867b8101164ac5/core/ipyflow/kernel/patched_nest_asyncio.py
import asyncio
import sys


def apply(loop=None):
    import nest_asyncio

    # ref: https://github.com/erdewit/nest_asyncio/issues/14
    nest_asyncio._patch_task = _patched_patch_task

    # ref: https://github.com/erdewit/nest_asyncio
    nest_asyncio.apply(loop=loop)


def _patched_patch_task():
    """Patch the Task's step and enter/leave methods to make it reentrant."""

    def step(task, exc=None):
        curr_task = curr_tasks.get(task._loop)
        try:
            step_orig(task, exc)
        finally:
            if curr_task is None:
                curr_tasks.pop(task._loop, None)
            else:
                curr_tasks[task._loop] = curr_task

    Task = asyncio.Task
    if sys.version_info >= (3, 7, 0):

        def enter_task(loop, task):
            curr_tasks[loop] = task

        def leave_task(loop, task):
            curr_tasks.pop(loop, None)

        asyncio.tasks._enter_task = enter_task
        asyncio.tasks._leave_task = leave_task
        curr_tasks = asyncio.tasks._current_tasks  # noqa
    else:
        curr_tasks = Task._current_tasks  # noqa
    try:
        step_orig = Task._Task__step  # noqa
        Task._Task__step = step  # noqa
    except AttributeError:
        try:
            step_orig = Task.__step  # noqa
            Task.__step = step  # noqa
        except AttributeError:
            step_orig = Task._step  # noqa
            Task._step = step  # noqa
