# lona-official-library

Official source packages for Lona.

Source files are organized under `src/<package>/`.
Each `.lo` file defines one module.
The repository includes a minimal build helper for compiling example programs against the package tree.

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

### `string`

Modules:

- `string/result`
- `string/view`
- `string/string`

### `algorithm`

Modules:

- `algorithm/order`
- `algorithm/search`
- `algorithm/sort`

### `diagnostic`

Modules:

- `diagnostic/fatal`
- `diagnostic/level`
- `diagnostic/diagnostic`

## Build

```bash
python3 tools/build.py examples/hello_console.lo --run
python3 tools/build.py examples/write_file.lo --run
python3 tools/build.py examples/copy_file.lo --run
python3 tools/build.py examples/container_vec.lo --run
python3 tools/build.py examples/container_list.lo --run
python3 tools/build.py examples/string_basic.lo --run
python3 tools/build.py examples/string_cow.lo --run
python3 tools/build.py examples/algorithm_search.lo --run
python3 tools/build.py examples/algorithm_sort.lo --run
python3 tools/build.py examples/diagnostic_basic.lo --run
```

Direct compiler invocation:

```bash
lac --cache-dir build/lona-cache -I src examples/hello_console.lo build/hello_console
```
