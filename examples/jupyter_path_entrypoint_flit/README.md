# entry_point_example_flit

A minimal example of a package which provides additional `jupyter_*_path`s
via `entry_points`, packaged with `flit`.

## Developing

### Setup

- ensure `flit` is installed

### Editable install

On any platform, enable live development by putting a `.pth` file in `site-packages`:

```bash
flit install --pth-file
```

On UNIX, a symlink may be used instead:

```bash
flint install --symlink
```

### Building

```bash
flit build
```

Optionally, set the `SOURCE_DATE_EPOCH` environment variable to ensure a
[reproducible](https://reproducible-builds.org) `.whl`.

> For example, to use the last `git` commit:
>
> ```bash
> SOURCE_DATE_EPOCH=$(git log -1 --format=%ct) flit build
> ```
