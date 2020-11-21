"""an example of using the jupyter_paths entry_point"""
import os

__version__ = "0.1.0"

HERE = os.path.abspath(os.path.dirname(__file__))

JUPYTER_CONFIG = [os.path.join(HERE, "etc", "jupyter")]
