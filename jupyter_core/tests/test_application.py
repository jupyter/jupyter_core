from jupyter_core import application

def test_basic():
    app = application.JupyterApp()

def test_default_traits():
    app = application.JupyterApp()
    for trait_name in app.traits():
        value = getattr(app, trait_name)
