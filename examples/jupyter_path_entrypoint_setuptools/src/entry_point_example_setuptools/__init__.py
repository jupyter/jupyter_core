"""an example of using the jupyter_*_paths entry_points in setuptools
"""
import time
__version__ = "0.1.0"

JUPYTER_CONFIG_PATH = "etc"
JUPYTER_DATA_PATH = "share"

# this is added to simulate a slow-loading import
time.sleep(1)
