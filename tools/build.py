#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a Lona program against the official package source tree."
    )
    parser.add_argument("source", help="Root .lo source file.")
    parser.add_argument(
        "output",
        nargs="?",
        help="Output binary path. Defaults to build/<source-stem>.",
    )
    parser.add_argument(
        "-I",
        "--include",
        action="append",
        default=[],
        help="Extra include directory. May be passed multiple times.",
    )
    parser.add_argument(
        "-O",
        "--opt",
        type=int,
        choices=range(0, 4),
        default=0,
        help="Optimization level passed to lac.",
    )
    parser.add_argument(
        "--target",
        help="Optional target triple passed to lac or lac-native.",
    )
    parser.add_argument(
        "--lto",
        choices=("off", "full"),
        default="off",
        help="LTO mode passed to lac or lac-native.",
    )
    parser.add_argument(
        "--compiler",
        default="lac",
        help="Compiler driver to invoke. Defaults to lac.",
    )
    parser.add_argument(
        "--cache-dir",
        help="Artifact cache directory passed to lac. Defaults to build/lona-cache.",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run the built binary after a successful build.",
    )
    return parser.parse_args()


def resolve_path(value: str, root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return root / path


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]

    source = resolve_path(args.source, repo_root)
    if not source.is_file():
        raise SystemExit(f"source not found: {source}")

    if args.output:
        output = resolve_path(args.output, repo_root)
    else:
        output = repo_root / "build" / source.stem

    if args.cache_dir:
        cache_dir = resolve_path(args.cache_dir, repo_root)
    else:
        cache_dir = repo_root / "build" / "lona-cache"

    include_dirs = [repo_root / "src"]
    for include_dir in args.include:
        include_dirs.append(resolve_path(include_dir, repo_root))

    output.parent.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    cmd = [args.compiler, "--cache-dir", str(cache_dir), "-O", str(args.opt)]
    if args.target:
        cmd.extend(["--target", args.target])
    if args.lto != "off":
        cmd.extend(["--lto", args.lto])
    for include_dir in include_dirs:
        cmd.extend(["-I", str(include_dir)])
    cmd.extend([str(source), str(output)])

    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=repo_root)

    if args.run:
        run_cmd = [str(output)]
        print("+", " ".join(run_cmd), flush=True)
        subprocess.run(run_cmd, check=True, cwd=repo_root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
