#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from repo_model import ROOT, dump_yaml, package_for_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Testa instalação APM em projeto Kiro temporário")
    parser.add_argument("--package", required=True)
    args = parser.parse_args()
    package = package_for_path(args.package)
    apm = shutil.which("apm")
    if not apm:
        raise SystemExit("APM CLI não encontrado no PATH")
    version = subprocess.run([apm, "--version"], check=False, text=True, capture_output=True)
    if version.returncode != 0 or "Agent Package Manager" not in (version.stdout + version.stderr):
        raise SystemExit("o comando apm encontrado não é o Agent Package Manager da Microsoft")

    with tempfile.TemporaryDirectory(prefix="atlas-apm-") as temporary:
        temp = Path(temporary)
        source = package.path
        expected = [package.name]

        if package.kind == "kit":
            source = temp / "kit"
            shutil.copytree(package.path, source)
            manifest = package.manifest.copy()
            dependencies = []
            expected = []
            for dependency in package.manifest["dependencies"]["apm"]:
                skill_path = ROOT / dependency["path"]
                dependencies.append({"path": skill_path.as_posix()})
                expected.append(skill_path.name)
            manifest["dependencies"] = {"apm": dependencies}
            dump_yaml(source / "apm.yml", manifest)

        consumer = temp / "consumer"
        consumer.mkdir()
        dump_yaml(
            consumer / "apm.yml",
            {
                "name": "atlas-smoke-test",
                "version": "1.0.0",
                "targets": ["kiro"],
                "dependencies": {"apm": [{"path": source.as_posix()}]},
            },
        )
        environment = os.environ.copy()
        subprocess.run([apm, "install", "--verbose"], cwd=consumer, env=environment, check=True)
        missing = [
            name for name in expected if not (consumer / ".kiro/skills" / name / "SKILL.md").is_file()
        ]
        if missing:
            print(f"Skills ausentes após instalação: {', '.join(missing)}")
            return 1
        print(f"OK: {package.name} instalou {len(expected)} skill(s) no Kiro")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
