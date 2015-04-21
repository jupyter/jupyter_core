from tempfile import NamedTemporaryFile

from traitlets import Integer

from jupyter_core.application import JupyterApp

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
    with NamedTemporaryFile(suffix='.py', mode='w') as f:
        f.write(_dummy_config)
        f.flush()
        app.initialize(['--config', f.name])
    assert app.config_file == f.name
    assert app.n == 10
