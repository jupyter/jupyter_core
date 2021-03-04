"""an example of using the jupyter_*_paths entry_points with flit"""
import os

__version__ = "0.1.0"

HERE = os.path.abspath(os.path.dirname(__file__))

JUPYTER_CONFIG_PATHS = [os.path.join(HERE, "etc", "jupyter")]
JUPYTER_DATA_PATHS = [os.path.join(HERE, "share", "jupyter")]
