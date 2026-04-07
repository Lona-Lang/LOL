# lona-official-library

Source-only official packages for Lona.

Packages live under `src/<package>/`.
Each `.lo` file is one module.
The builder stays thin because Lona already does top-down dependency analysis and incremental compilation.

## Packages

### `ios`

Modules:

- `ios/result`
- `ios/stream`
- `ios/file`
- `ios/console`

### `container`

Modules:

- `container/result`
- `container/slice`
- `container/vec`
- `container/list`

## Build

```bash
python3 tools/build.py examples/hello_console.lo --run
python3 tools/build.py examples/write_file.lo --run
python3 tools/build.py examples/copy_file.lo --run
python3 tools/build.py examples/container_vec.lo --run
python3 tools/build.py examples/container_list.lo --run
```

Direct compiler use:

```bash
lac --cache-dir build/lona-cache -I src examples/hello_console.lo build/hello_console
```
