Changes in jupyter-core
=======================

4.3
---

4.3.0
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.3.0>`__

- Add `JUPYTER_NO_CONFIG` environment variable for disabling all Jupyter configuration.
- More detailed error message when failing to launch subcommands.


4.2
---

4.2.1
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.2.1>`__

- Fix error message on Windows when subcommand not found.
- Correctly display PATH in ``jupyter troubleshoot`` on Windows.

4.2.0
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.2.0>`__

- Make :command:`jupyter` directory top priority in search path for subcommands,
  so that :command:`jupyter-subcommand` next to :command:`jupyter` will always be picked if present.
- Avoid using ``shell=True`` for subcommand dispatch on Windows.

4.1
---

4.1.1
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.1.1>`__

- Include symlink directory and real location on subcommand PATH when :file:`jupyter` is a symlink.


4.1.0
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.1>`__

- Add ``jupyter.py`` module, so that :command:`python -m jupyter` always works.
- Add prototype ``jupyter troubleshoot`` command for displaying environment info.
- Ensure directory containing ``jupyter`` executable is included when dispatching subcommands.
- Unicode fixes for Legacy Python.


4.0
---

4.0.6
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.0.6>`__

-  fix typo preventing migration when custom.css is missing

4.0.5
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.0.5>`__

-  fix subcommands on Windows (yes, again)
-  fix migration when custom.js/css are not present

4.0.4
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.0.4>`__

-  fix subcommands on Windows (again)
-  ensure ``jupyter --version`` outputs to stdout

4.0.3
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.0.3>`__

-  setuptools fixes needed to run on Windows

4.0.2
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.0.2>`__

-  fixes for jupyter-migrate

4.0.1
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.0.1>`__

This is the first release of the jupyter-core package.
