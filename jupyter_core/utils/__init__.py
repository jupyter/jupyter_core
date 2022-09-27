# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import errno
import inspect
import os
import sys
import warnings
from pathlib import Path


def ensure_dir_exists(path, mode=0o777):
    """ensure that a directory exists
    If it doesn't exist, try to create it, protecting against a race condition
    if another process is doing the same.
    The default permissions are determined by the current umask.
    """
    try:
        os.makedirs(path, mode=mode)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    if not os.path.isdir(path):
        raise OSError("%r exists but is not a directory" % path)


def _get_frame(level):
    """Get the frame at the given stack level."""
    # sys._getframe is much faster than inspect.stack, but isn't guaranteed to
    # exist in all python implementations, so we fall back to inspect.stack()

    # We need to add one to level to account for this get_frame call.
    if hasattr(sys, "_getframe"):
        frame = sys._getframe(level + 1)
    else:
        frame = inspect.stack(context=0)[level + 1].frame
    return frame


# This function is from https://github.com/python/cpython/issues/67998
# (https://bugs.python.org/file39550/deprecated_module_stacklevel.diff) and
# calculates the appropriate stacklevel for deprecations to target the
# deprecation for the caller, no matter how many internal stack frames we have
# added in the process. For example, with the deprecation warning in the
# __init__ below, the appropriate stacklevel will change depending on how deep
# the inheritance hierarchy is.
def _external_stacklevel(internal):
    """Find the stacklevel of the first frame that doesn't contain any of the given internal strings

    The depth will be 1 at minimum in order to start checking at the caller of
    the function that called this utility method.
    """
    # Get the level of my caller's caller
    level = 2
    frame = _get_frame(level)

    # Normalize the path separators:
    normalized_internal = [str(Path(s)) for s in internal]

    # climb the stack frames while we see internal frames
    while frame and any(s in str(Path(frame.f_code.co_filename)) for s in normalized_internal):
        level += 1
        frame = frame.f_back

    # Return the stack level from the perspective of whoever called us (i.e., one level up)
    return level - 1


def deprecation(message, internal="jupyter_core/"):
    """Generate a deprecation warning targeting the first frame that is not 'internal'

    internal is a string or list of strings, which if they appear in filenames in the
    frames, the frames will be considered internal. Changing this can be useful if, for examnple,
    we know that our internal code is calling out to another library.
    """
    if isinstance(internal, str):
        internal = [internal]

    # stack level of the first external frame from here
    stacklevel = _external_stacklevel(internal)

    # The call to .warn adds one frame, so bump the stacklevel up by one
    warnings.warn(message, DeprecationWarning, stacklevel=stacklevel + 1)
