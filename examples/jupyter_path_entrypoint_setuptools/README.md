# entry_point_example_setuptools

A minimal example of a package which provides additional `jupyter_*_path`s
via `entry_points`, packaged with `setuptools`.

## Developing

### Setup

- ensure `pip` is installed

### Editable install

```bash
pip install -e .
```

### Building

```bash
python setup.py sdist bdist_wheel
```
