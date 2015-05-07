import os
import shutil
from tempfile import mkdtemp

from traitlets import Integer

from jupyter_core.application import JupyterApp

pjoin = os.path.join


def test_basic():
    app = JupyterApp()


def test_default_traits():
    app = JupyterApp()
    for trait_name in app.traits():
        value = getattr(app, trait_name)

class DummyApp(JupyterApp):
    n = Integer(0, config=True)

_dummy_config = """
c.DummyApp.n = 10
"""

def test_custom_config():
    app = DummyApp()
    td = mkdtemp()
    fname = pjoin(td, 'config.py')
    with open(fname, 'w') as f:
        f.write(_dummy_config)
    app.initialize(['--config', fname])
    shutil.rmtree(td)
    assert app.config_file == fname
    assert app.n == 10


def test_cli_override():
    app = DummyApp()
    td = mkdtemp()
    fname = pjoin(td, 'config.py')
    with open(fname, 'w') as f:
        f.write(_dummy_config)
    app.initialize(['--config', fname, '--DummyApp.n=20'])
    shutil.rmtree(td)
    assert app.n == 20
