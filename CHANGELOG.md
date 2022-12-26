# Changes in jupyter-core

<!-- <START NEW CHANGELOG ENTRY> -->

## 5.1.1

([Full Changelog](https://github.com/jupyter/jupyter_core/compare/v5.1.0...1ed25e389116fbb98c513ee2148f38f9548e6198))

### Enhancements made

- Only prefer envs owned by the current user [#323](https://github.com/jupyter/jupyter_core/pull/323) ([@minrk](https://github.com/minrk))

### Bugs fixed

- Don't treat the conda root env as an env [#324](https://github.com/jupyter/jupyter_core/pull/324) ([@minrk](https://github.com/minrk))

### Maintenance and upkeep improvements

- Fix lint [#325](https://github.com/jupyter/jupyter_core/pull/325) ([@blink1073](https://github.com/blink1073))
- Adopt ruff and address lint [#321](https://github.com/jupyter/jupyter_core/pull/321) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/jupyter_core/graphs/contributors?from=2022-11-28&to=2022-12-22&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Ablink1073+updated%3A2022-11-28..2022-12-22&type=Issues) | [@jasongrout](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Ajasongrout+updated%3A2022-11-28..2022-12-22&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Aminrk+updated%3A2022-11-28..2022-12-22&type=Issues) | [@pre-commit-ci](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Apre-commit-ci+updated%3A2022-11-28..2022-12-22&type=Issues)

<!-- <END NEW CHANGELOG ENTRY> -->

## 5.1.0

([Full Changelog](https://github.com/jupyter/jupyter_core/compare/v5.0.0...9a976bb7d4f2d7092b2ee98b05a30eb1ff0be425))

### Enhancements made

- Add run_sync and ensure_async functions [#315](https://github.com/jupyter/jupyter_core/pull/315) ([@davidbrochart](https://github.com/davidbrochart))

### Maintenance and upkeep improvements

- Add more path tests [#316](https://github.com/jupyter/jupyter_core/pull/316) ([@blink1073](https://github.com/blink1073))
- Clean up workflows and add badges [#314](https://github.com/jupyter/jupyter_core/pull/314) ([@blink1073](https://github.com/blink1073))
- CI Cleanup [#312](https://github.com/jupyter/jupyter_core/pull/312) ([@blink1073](https://github.com/blink1073))

### Documentation improvements

- Clean up workflows and add badges [#314](https://github.com/jupyter/jupyter_core/pull/314) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/jupyter_core/graphs/contributors?from=2022-11-09&to=2022-11-28&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Ablink1073+updated%3A2022-11-09..2022-11-28&type=Issues) | [@davidbrochart](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Adavidbrochart+updated%3A2022-11-09..2022-11-28&type=Issues) | [@pre-commit-ci](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Apre-commit-ci+updated%3A2022-11-09..2022-11-28&type=Issues)

## 5.0.0

([Full Changelog](https://github.com/jupyter/jupyter_core/compare/4.9.2...fdbb55b59575a3eb6aeb502998a835b013401412))

### Major Changes

#### Prefer Environment Level Configuration

We now make the assumption that if we are running in a virtual environment, we should prioritize the environment-level `sys.prefix` over the user-level paths. Users can opt out of this behavior by setting `JUPYTER_PREFER_ENV_PATH`, which takes precedence over our autodetection.

#### Migrate to Standard Platform Directories

In version 5, we introduce a `JUPYTER_PLATFORM_DIRS` environment variable to opt in to using more appropriate platform-specific directories.  We raise a deprecation warning if the variable is not set.  In version 6,  `JUPYTER_PLATFORM_DIRS` will be opt-out.  In version 7, we will remove the environment variable checks and old directory logic.

#### Drop Support for Python 3.7

We are dropping support for Python 3.7 ahead of its official end of life, to reduce maintenance burden as we add support for Python 3.11.

### Enhancements made

- Use platformdirs for path locations [#292](https://github.com/jupyter/jupyter_core/pull/292) ([@blink1073](https://github.com/blink1073))
- Try to detect if we are in a virtual environment and change path precedence accordingly [#286](https://github.com/jupyter/jupyter_core/pull/286) ([@jasongrout](https://github.com/jasongrout))

### Bugs fixed

- Add current working directory as first config path [#291](https://github.com/jupyter/jupyter_core/pull/291) ([@blink1073](https://github.com/blink1073))
- Fix inclusion of jupyter file and check in CI [#276](https://github.com/jupyter/jupyter_core/pull/276) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- Bump github/codeql-action from 1 to 2 [#308](https://github.com/jupyter/jupyter_core/pull/308) ([@dependabot](https://github.com/dependabot))
- Bump actions/checkout from 2 to 3 [#307](https://github.com/jupyter/jupyter_core/pull/307) ([@dependabot](https://github.com/dependabot))
- Add dependabot [#306](https://github.com/jupyter/jupyter_core/pull/306) ([@blink1073](https://github.com/blink1073))
- Adopt jupyter releaser [#305](https://github.com/jupyter/jupyter_core/pull/305) ([@blink1073](https://github.com/blink1073))
- Add more typing [#304](https://github.com/jupyter/jupyter_core/pull/304) ([@blink1073](https://github.com/blink1073))
- Require Python 3.8+ [#302](https://github.com/jupyter/jupyter_core/pull/302) ([@blink1073](https://github.com/blink1073))
- Use hatch backend [#265](https://github.com/jupyter/jupyter_core/pull/265) ([@blink1073](https://github.com/blink1073))
- Switch to flit build backend [#262](https://github.com/jupyter/jupyter_core/pull/262) ([@blink1073](https://github.com/blink1073))
- is_hidden: Use normalized paths [#271](https://github.com/jupyter/jupyter_core/pull/271) ([@martinRenou](https://github.com/martinRenou))
-

### Documentation

- Update broken link to `Contributing` guide [#289](https://github.com/jupyter/jupyter_core/pull/289) ([@jamesr66a](https://github.com/jamesr66a))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/jupyter_core/graphs/contributors?from=2022-02-15&to=2022-11-09&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Ablink1073+updated%3A2022-02-15..2022-11-09&type=Issues) | [@bollwyvl](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Abollwyvl+updated%3A2022-02-15..2022-11-09&type=Issues) | [@dependabot](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Adependabot+updated%3A2022-02-15..2022-11-09&type=Issues) | [@dlqqq](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Adlqqq+updated%3A2022-02-15..2022-11-09&type=Issues) | [@gaborbernat](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Agaborbernat+updated%3A2022-02-15..2022-11-09&type=Issues) | [@gutow](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Agutow+updated%3A2022-02-15..2022-11-09&type=Issues) | [@jamesr66a](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Ajamesr66a+updated%3A2022-02-15..2022-11-09&type=Issues) | [@jaraco](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Ajaraco+updated%3A2022-02-15..2022-11-09&type=Issues) | [@jasongrout](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Ajasongrout+updated%3A2022-02-15..2022-11-09&type=Issues) | [@kevin-bates](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Akevin-bates+updated%3A2022-02-15..2022-11-09&type=Issues) | [@maartenbreddels](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Amaartenbreddels+updated%3A2022-02-15..2022-11-09&type=Issues) | [@martinRenou](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3AmartinRenou+updated%3A2022-02-15..2022-11-09&type=Issues) | [@meeseeksmachine](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Ameeseeksmachine+updated%3A2022-02-15..2022-11-09&type=Issues) | [@pre-commit-ci](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_core+involves%3Apre-commit-ci+updated%3A2022-02-15..2022-11-09&type=Issues)

## 5.0.0rc0

[on
GitHub](https://github.com/jupyter/jupyter_core/releases/tag/5.0.0rc0)

- Try to detect if we are in a virtual environment and change path
  precedence accordingly. ([#286](https://github.com/jupyter/jupyter_core/pull/286))
- Update broken link to Contributing guide.
  ([#289](https://github.com/jupyter/jupyter_core/pull/289))
- Add current working directory as first config path.
  ([#291](https://github.com/jupyter/jupyter_core/pull/291))
- Use platformdirs for path locations. ([#292](https://github.com/jupyter/jupyter_core/pull/292))

## 4.11

### 4.11.1

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.11.1)

- Fix inclusion of jupyter file and check in CI.
  ([#276](https://github.com/jupyter/jupyter_core/pull/276))

### 4.11.0

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.11.0)

- Use hatch build backend. ([#265](https://github.com/jupyter/jupyter_core/pull/265))
- `is_hidden`: Use normalized paths. ([#271](https://github.com/jupyter/jupyter_core/pull/271))

## 4.10

### 4.10.0

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.10.0)

- Include all files from `jupyter_core`. ([#253](https://github.com/jupyter/jupyter_core/pull/253))
- Add project URLs to `setup.cfg`. ([#254](https://github.com/jupyter/jupyter_core/pull/254))
- Set up pre-commit. ([#255](https://github.com/jupyter/jupyter_core/pull/255))
- Add flake8 and mypy settings. ([#256](https://github.com/jupyter/jupyter_core/pull/256))
- Clean up CI. ([#258](https://github.com/jupyter/jupyter_core/pull/258))

## 4.9

### 4.9.2

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.9.1)

- Set proper `sys.argv[0]` for subcommand. ([#248](https://github.com/jupyter/jupyter_core/pull/248))
- Add explicit encoding in open calls. ([#249](https://github.com/jupyter/jupyter_core/pull/249))
- `jupyter_config_dir` - reorder `home_dir` initialization.
  ([#251](https://github.com/jupyter/jupyter_core/pull/251))

### 4.9.1

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.9.0)

- Add a workaround for virtualenv for getting the user site directory.
  ([#247](https://github.com/jupyter/jupyter_core/pull/247))

### 4.9.0

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.9.0)

See the [jupyter_core
4.9](https://github.com/jupyter/jupyter_core/milestone/21?closed=1)
milestone on GitHub for the full list of pull requests and issues
closed.

- Add Python site user base subdirectories to config and data
  user-level paths if `site.ENABLE_USER_SITE` is True. One way to
  disable these directory additions is to set the `PYTHONNOUSERSITE`
  environment variable. These locations can be customized by setting
  the `PYTHONUSERBASE` environment variable. ([#242](https://github.com/jupyter/jupyter_core/pull/242))

## 4.8

### 4.8.2

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.8.2)

jupyter_core 4.8.1 was released the same day as 4.8.0 and also included
the fix below for the Windows tests. Unfortunately, the 4.8.1 release
commit and tag were not pushed to GitHub. We are releasing 4.8.2 so we
have a commit and tag in version control.

- Fix windows test regression ([#240](https://github.com/jupyter/jupyter_core/pull/240))

### 4.8.0

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.8.0)

See the [jupyter_core
4.8](https://github.com/jupyter/jupyter_core/milestone/20?closed=1)
milestone on GitHub for the full list of pull requests and issues
closed.

jupyter-core now has experimental support for PyPy (Python 3.7). Some
features are known not to work due to limitations in PyPy, such as
hidden file detection on Windows.

- Print an error message instead of an exception when a command is not
  found ([#218](https://github.com/jupyter/jupyter_core/pull/218))
- Return canonical path when using `%APPDATA%` on Windows
  ([#222](https://github.com/jupyter/jupyter_core/pull/222))
- Print full usage on missing or invalid commands
  ([#225](https://github.com/jupyter/jupyter_core/pull/225))
- Remove dependency on `pywin32` package on PyPy
  ([#230](https://github.com/jupyter/jupyter_core/pull/230))
- Update packages listed in `jupyter --version`
  ([#232](https://github.com/jupyter/jupyter_core/pull/232))
- Inherit base aliases/flags from traitlets Application, including
  `--show-config` from traitlets 5 ([#233](https://github.com/jupyter/jupyter_core/pull/233))
- Trigger warning when trying to check hidden file status on PyPy
  ([#238](https://github.com/jupyter/jupyter_core/pull/238))

## 4.7

### 4.7.1

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.7.1)

- Allow creating user to delete secure file ([#213](https://github.com/jupyter/jupyter_core/pull/213))

### 4.7.0

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.7.0)

See the [jupyter_core
4.7](https://github.com/jupyter/jupyter_core/milestone/19?closed=1)
milestone on GitHub for the full list of pull requests and issues
closed.

- Add a new `JUPYTER_PREFER_ENV_PATH` variable, which can be set to
  switch the order of the environment-level path and the user-level
  path in the Jupyter path hierarchy (e.g., `jupyter --paths`). It is
  considered set if it is a value that is not one of 'no', 'n',
  'off', 'false', '0', or '0.0' (case insensitive). If you are
  running Jupyter in multiple virtual environments as the same user,
  you will likely want to set this environment variable.
- Drop Python 2.x and 3.5 support, as they have reached end of life.
- Add Python 3.9 builds to testing, and expand testing to cover
  Windows, macOS, and Linux platforms.
- `jupyter --paths --debug` now explains the environment variables
  that affect the current path list.
- Update the file hidden check on Windows to use new Python features
  rather than ctypes directly.
- Add conda environment information in `jupyter troubleshoot`.
- Update `_version.version_info` and `_version.__version__` to follow
  Python conventions.

## 4.6

### 4.6.3

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.6.3)

- Changed windows secure_write path to skip all filesystem permission
  checks when running in insecure mode. Too many exception paths
  existed for mounted file systems to reliably try to set them before
  opting out with the insecure write pattern.

### 4.6.2

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.6.2)

- Add ability to allow insecure writes with
  JUPYTER_ALLOW_INSECURE_WRITES environement variable
  ([#182](https://github.com/jupyter/jupyter_core/pull/182)).
- Docs typo and build fixes
- Added python 3.7 and 3.8 builds to testing

### 4.6.1

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.6.1)

- Tolerate execute bit in owner permissions when validating secure
  writes ([#173](https://github.com/jupyter/jupyter_core/pull/173)).
- Fix project name typo in copyright ([#171](https://github.com/jupyter/jupyter_core/pull/171)).

### 4.6.0

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.6.0)

- Unicode characters existing in the user's home directory name are
  properly handled ([#131](https://github.com/jupyter/jupyter_core/pull/131)).
- `mock` is now only required for testing on Python 2
  ([#157](https://github.com/jupyter/jupyter_core/pull/157)).
- Deprecation warnings relative to `_runtime_dir_changed` are no
  longer produced ([#158](https://github.com/jupyter/jupyter_core/pull/158)).
- The `scripts` directory relative to the current python environment
  is now appended to the search directory for subcommands
  ([#162](https://github.com/jupyter/jupyter_core/pull/162)).
- Some utility functions (`exists()`, `is_hidden()`, `secure_write()`)
  have been moved from `jupyter_client` and `jupyter_server` to
  `jupyter_core` ([#163](https://github.com/jupyter/jupyter_core/pull/163)).
- Fix error on Windows when setting private permissions
  ([#166](https://github.com/jupyter/jupyter_core/pull/166)).

## 4.5

### 4.5.0

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.5.0)

- `jupyter --version` now tries to show the version number of various
  other installed Jupyter packages, not just `jupyter_core`
  ([#136](https://github.com/jupyter/jupyter_core/pull/136)). This will hopefully make
  it clearer that there are various packages with their own version
  numbers.
- Allow a `JUPYTER_CONFIG_PATH`
  environment variable to specify a search path of additional
  locations for config ([#139](https://github.com/jupyter/jupyter_core/pull/139)).
- `jupyter subcommand` no longer modifies the `PATH` environment variable when it runs
  `jupyter-subcommand` ([#148](https://github.com/jupyter/jupyter_core/pull/148)).
- Jupyter's 'runtime' directory no longer uses `XDG_RUNTIME_DIR`
  ([#143](https://github.com/jupyter/jupyter_core/pull/143)). While it has some
  attractive properties, it has led to various problems; see the pull
  request for details.
- Fix `JupyterApp` to respect the `raise_config_file_errors` traitlet
  ([#149](https://github.com/jupyter/jupyter_core/pull/149)).
- Various improvements to the bash completion scripts in this
  repository ([#125](https://github.com/jupyter/jupyter_core/pull/125),
  [#126](https://github.com/jupyter/jupyter_core/pull/126)).
- The `setup.py` script now always uses setuptools, like most other
  Jupyter projects ([#147](https://github.com/jupyter/jupyter_core/pull/147)).
- The LICENSE file is included in wheels ([#133](https://github.com/jupyter/jupyter_core/pull/133)).

## 4.4

### 4.4.0

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.4.0)

- `jupyter troubleshoot` gets the list of packages from the Python
  environment it's in, by using `sys.executable` to call `pip list`
  ([#104](https://github.com/jupyter/jupyter_core/pull/104)).
- Added utility function `ensure_dir_exists`, and switched to using it
  over the one from ipython_genutils, which does permissions wrong
  ([#113](https://github.com/jupyter/jupyter_core/pull/113)).
- Avoid creating the `~/.ipython` directory when checking if it exists
  for config migration ([#118](https://github.com/jupyter/jupyter_core/pull/118)).
- Fix mistaken description in zsh completions ([#98](https://github.com/jupyter/jupyter_core/pull/98)).
- Fix subcommand tests on Windows ([#103](https://github.com/jupyter/jupyter_core/pull/103)).
- The README now describes how to work on `jupyter_core` and build the
  docs ([#110](https://github.com/jupyter/jupyter_core/pull/110)).
- Fix a broken link to a release in the docs ([#109](https://github.com/jupyter/jupyter_core/pull/109)).

## 4.3

### 4.3.0

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.3.0)

- Add `JUPYTER_NO_CONFIG` environment variable for
  disabling all Jupyter configuration.
- More detailed error message when failing to launch subcommands.

## 4.2

### 4.2.1

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.2.1)

- Fix error message on Windows when subcommand not found.
- Correctly display PATH in `jupyter troubleshoot` on Windows.

### 4.2.0

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.2.0)

- Make `jupyter` directory top
  priority in search path for subcommands, so that
  `jupyter-subcommand` next to
  `jupyter` will always be picked if
  present.
- Avoid using `shell=True` for subcommand dispatch on Windows.

## 4.1

### 4.1.1

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.1.1)

- Include symlink directory and real location on subcommand PATH when
  `jupyter` is a symlink.

### 4.1.0

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.1.0)

- Add `jupyter.py` module, so that
  `python -m jupyter` always works.
- Add prototype `jupyter troubleshoot` command for displaying
  environment info.
- Ensure directory containing `jupyter` executable is included when
  dispatching subcommands.
- Unicode fixes for Legacy Python.

## 4.0

### 4.0.6

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.0.6)

- fix typo preventing migration when custom.css is missing

### 4.0.5

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.0.5)

- fix subcommands on Windows (yes, again)
- fix migration when custom.js/css are not present

### 4.0.4

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.0.4)

- fix subcommands on Windows (again)
- ensure `jupyter --version` outputs to stdout

### 4.0.3

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.0.3)

- setuptools fixes needed to run on Windows

### 4.0.2

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.0.2)

- fixes for jupyter-migrate

### 4.0.1

[on GitHub](https://github.com/jupyter/jupyter_core/releases/tag/4.0.1)

This is the first release of the jupyter-core package.
