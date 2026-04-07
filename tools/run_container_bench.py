#!/usr/bin/env python3

from __future__ import annotations

import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=cwd)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    build_dir = repo_root / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    lona_bin = build_dir / "container_bench_lona"
    cpp_bin = build_dir / "container_bench_cpp"

    print("== Lona -O2 ==", flush=True)
    run(
        [
            "python3",
            "tools/build.py",
            "examples/container_bench.lo",
            str(lona_bin),
            "-O",
            "2",
        ],
        repo_root,
    )
    run([str(lona_bin)], repo_root)

    print("== C++ -O2 ==", flush=True)
    run(
        [
            "c++",
            "-std=c++20",
            "-O2",
            "benchmarks/container_bench.cpp",
            "-o",
            str(cpp_bin),
        ],
        repo_root,
    )
    run([str(cpp_bin)], repo_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
