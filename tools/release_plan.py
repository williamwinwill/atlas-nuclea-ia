#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess

from repo_model import discover_packages, package_matrix, tag_exists


def main() -> None:
    parser = argparse.ArgumentParser(description="Lista versões ainda não publicadas")
    parser.add_argument("--kind", choices=("skill", "kit"), required=True)
    parser.add_argument(
        "--include-incomplete",
        action="store_true",
        help="inclui tags existentes que ainda não possuem GitHub Release",
    )
    args = parser.parse_args()
    pending = []
    for package in discover_packages():
        if package.kind != args.kind:
            continue
        tag = f"{package.name}--v{package.version}"
        if not tag_exists(tag):
            pending.append(package)
            continue
        if args.include_incomplete:
            release = subprocess.run(
                ["gh", "release", "view", tag],
                check=False,
                text=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if release.returncode != 0:
                pending.append(package)
    print(package_matrix(pending))


if __name__ == "__main__":
    main()
