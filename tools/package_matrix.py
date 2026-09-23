#!/usr/bin/env python3
from __future__ import annotations

import argparse

from repo_model import affected_packages, package_matrix


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera matrix JSON de pacotes APM")
    parser.add_argument("--base", help="ref Git usada para selecionar pacotes afetados")
    args = parser.parse_args()
    print(package_matrix(affected_packages(args.base)))


if __name__ == "__main__":
    main()

