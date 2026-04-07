# lona-official-library

This repository hosts source-only official packages for Lona.
It is not a monolithic standard library.

Packages live under `src/<package>/`, and each `.lo` file is one module.
Because Lona already resolves imports top-down and supports incremental compilation, the builder in this repo stays intentionally thin.

## Current package

### `ios`

`ios` is the first official package.
Its public API is shaped for Lona first, not as a direct `stdio.h` mirror.

Current public modules:

- `ios/result`: `Status` and generic `Result[T] { value, status }`
- `ios/stream`: `TextSink`, `ByteSource`, `ByteSink`, and generic helpers such as `write_line_to[T]`, `copy_once[T]`, and `copy_all[T]`
- `ios/file`: `File`, `FilePath`, `path(...)`, `temporary()`, and instance operations on both file handles and file paths
- `ios/console`: console-oriented helpers such as `standard_output`, `write_line`, `error_line`, `flush`

Current compiler-stable consumption pattern:

- `Status` values are consumed directly with methods such as `status.failed()`.
- `Result[T]` values can now be consumed directly with methods such as `opened.failed()` and `opened.code()`.

Internal implementation module:

- `ios/_c`: hosted Linux/x86_64 `C FFI v0` bindings hidden behind the public API

What this version already does:

- exposes a reusable `File` type instead of raw `FILE*`
- groups path-based file system operations under `FilePath` instead of a flat top-level function list
- uses generic `Result[T] { value, status }` for open/read/write operations
- uses trait-based text and byte stream abstractions via `stream.TextSink`, `stream.ByteSource`, and `stream.ByteSink`
- provides reusable buffered copy helpers via `stream.copy_once[T]` and `stream.copy_all[T]`
- provides borrowed console streams without forcing users onto C names

Not included yet:

- varargs formatting APIs
- richer buffer/string abstractions beyond `u8 const[*]`
- non-Linux hosted targets

## Layout

- `src/ios/result.lo`
- `src/ios/stream.lo`
- `src/ios/file.lo`
- `src/ios/console.lo`
- `src/ios/_c.lo`
- `examples/hello_console.lo`
- `examples/write_file.lo`
- `examples/copy_file.lo`
- `tools/build.py`

## Build examples

Build and run the console example:

```bash
python3 tools/build.py examples/hello_console.lo --run
```

Build and run the file output example:

```bash
python3 tools/build.py examples/write_file.lo --run
```

Build and run the buffered copy example:

```bash
python3 tools/build.py examples/copy_file.lo --run
```

Equivalent direct compiler invocation:

```bash
lac --cache-dir build/lona-cache -I src examples/hello_console.lo build/hello_console
```

## Importing

```lona
import ios/console

var status = console.write_line("hello from ios")
if status.failed() {
    ret status.code
}

ret 0
```

To work against a generic text sink:

```lona
import ios/file
import ios/stream

var opened = file.path("build/demo.txt").create()
if opened.failed() {
    ret opened.code()
}

var status = stream.write_line_to[file.File](ref opened.value, "hello")
if status.failed() {
    ret status.code
}

ret 0
```

To copy bytes between two generic streams:

```lona
import ios/file
import ios/stream

var source = file.path("examples/source.txt").open()
if source.failed() {
    ret source.code()
}

var target = file.path("build/copied-source.txt").create()
if target.failed() {
    ret target.code()
}

var buffer u8[32] = {}
var copied = stream.copy_all[file.File, file.File](ref source.value, ref target.value, &buffer(0), 32)
if copied.failed() {
    ret copied.code()
}

ret 0
```
