# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
# Note: copied from https://github.com/ipyflow/ipyflow/blob/8e4bc5cb8d4231b9b69f4f9dce867b8101164ac5/core/ipyflow/kernel/patched_nest_asyncio.py
import asyncio


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
    if hasattr(Task, '_nest_patched'):
        return
    def enter_task(loop, task):
        curr_tasks[loop] = task

    def leave_task(loop, task):
        curr_tasks.pop(loop, None)

    asyncio.tasks._enter_task = enter_task
    asyncio.tasks._leave_task = leave_task
    curr_tasks = asyncio.tasks._current_tasks  # type: ignore
    try:
        step_orig = Task._Task__step  # type: ignore
        Task._Task__step = step  # type: ignore
    except AttributeError:
        try:
            step_orig = Task.__step  # type: ignore
            Task.__step = step  # type: ignore
        except AttributeError:
            step_orig = Task._step  # type: ignore
            Task._step = step  # type: ignore
    Task._nest_patched = True  # type: ignore
