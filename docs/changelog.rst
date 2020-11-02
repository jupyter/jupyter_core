Changes in jupyter-core
=======================


4.7
---
`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.7>`__

See the `jupyter_core
4.7 <https://github.com/jupyter/jupyter_core/milestone/19?closed=1>`__
milestone on GitHub for the full list of pull requests and issues closed.

- Add a new ``JUPYTER_PREFER_ENV_PATH`` variable, which can be set to switch the order of the environment-level path and the user-level path in the Jupyter path hierarchy (e.g., ``jupyter --paths``). It is considered set if it is a value that is not one of 'no', 'n', 'off', 'false', '0', or '0.0' (case insensitive). If you are running Jupyter in multiple virtual environments as the same user, you will likely want to set this environment variable.
- Drop Python 2.x and 3.5 support, as they have reached end of life.
- Add Python 3.9 builds to testing, and expand testing to cover Windows, macOS, and Linux platforms.
- ``jupyter --paths --debug`` now explains the environment variables that affect the current path list.
- Update the file hidden check on Windows to use new Python features rather than ctypes directly.
- Add conda environment information in ``jupyter troubleshoot``.
- Update ``_version.version_info`` and ``_version.__version__`` to follow Python conventions.

4.6
---

4.6.3
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.6.3>`__

- Changed windows secure_write path to skip all filesystem permission checks when running in insecure mode.
  Too many exception paths existed for mounted file systems to reliably try to set them before opting out with the insecure write pattern.


4.6.2
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.6.2>`__

- Add ability to allow insecure writes with JUPYTER_ALLOW_INSECURE_WRITES environement variable (:ghpull:`182`).
- Docs typo and build fixes
- Added python 3.7 and 3.8 builds to testing

4.6.1
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.6.1>`__

- Tolerate execute bit in owner permissions when validating secure writes (:ghpull:`173`).
- Fix project name typo in copyright (:ghpull:`171`).

4.6.0
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.6.0>`__

- Unicode characters existing in the user's home directory name are properly
  handled (:ghpull:`131`).
- ``mock`` is now only required for testing on Python 2 (:ghpull:`157`).
- Deprecation warnings relative to ``_runtime_dir_changed`` are no longer
  produced (:ghpull:`158`).
- The ``scripts`` directory relative to the current python environment is
  now appended to the search directory for subcommands (:ghpull:`162`).
- Some utility functions (``exists()``, ``is_hidden()``, ``secure_write()``)
  have been moved from ``jupyter_client`` and ``jupyter_server`` to
  ``jupyter_core`` (:ghpull:`163`).
- Fix error on Windows when setting private permissions (:ghpull:`166`).

4.5
---

4.5.0
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.5.0>`__

- ``jupyter --version`` now tries to show the version number of various other
  installed Jupyter packages, not just ``jupyter_core`` (:ghpull:`136`).
  This will hopefully make it clearer that there are various packages with
  their own version numbers.
- Allow a :envvar:`JUPYTER_CONFIG_PATH` environment variable to specify a
  search path of additional locations for config (:ghpull:`139`).
- ``jupyter subcommand`` no longer modifies the :envvar:`PATH` environment
  variable when it runs ``jupyter-subcommand`` (:ghpull:`148`).
- Jupyter's 'runtime' directory no longer uses ``XDG_RUNTIME_DIR``
  (:ghpull:`143`). While it has some attractive properties, it has led to
  various problems; see the pull request for details.
- Fix ``JupyterApp`` to respect the ``raise_config_file_errors`` traitlet
  (:ghpull:`149`).
- Various improvements to the bash completion scripts in this repository
  (:ghpull:`125`, :ghpull:`126`).
- The ``setup.py`` script now always uses setuptools, like most other Jupyter
  projects (:ghpull:`147`).
- The LICENSE file is included in wheels (:ghpull:`133`).

4.4
---

4.4.0
~~~~~

`on
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.4.0>`__

- ``jupyter troubleshoot`` gets the list of packages from the Python environment
  it's in, by using ``sys.executable`` to call ``pip list`` (:ghpull:`104`).
- Added utility function ``ensure_dir_exists``, and switched to using it over
  the one from ipython_genutils, which does permissions wrong (:ghpull:`113`).
- Avoid creating the ``~/.ipython`` directory when checking if it exists for
  config migration (:ghpull:`118`).
- Fix mistaken description in zsh completions (:ghpull:`98`).
- Fix subcommand tests on Windows (:ghpull:`103`).
- The README now describes how to work on ``jupyter_core`` and build the docs
  (:ghpull:`110`).
- Fix a broken link to a release in the docs (:ghpull:`109`).

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
GitHub <https://github.com/jupyter/jupyter_core/releases/tag/4.1.0>`__

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
