#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date

from repo_model import ROOT, bump_semver, discover_packages, dump_yaml, load_config, load_yaml, tag_exists


def desired_dependencies(include_unreleased: bool = False) -> list[dict[str, str]]:
    repository = str(load_config()["repository"])
    dependencies: list[dict[str, str]] = []
    for package in discover_packages():
        if package.kind != "skill":
            continue
        tag = f"{package.name}--v{package.version}"
        if not include_unreleased and not tag_exists(tag):
            continue
        dependencies.append({"git": repository, "path": package.relative_path, "ref": tag})
    return sorted(dependencies, key=lambda item: item["path"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Sincroniza kits/all com skills publicadas")
    parser.add_argument("--check", action="store_true", help="não escreve e falha se houver drift")
    parser.add_argument("--include-unreleased", action="store_true", help="inclui manifests mesmo sem tag local")
    args = parser.parse_args()

    manifest_path = ROOT / "kits/all/apm.yml"
    manifest = load_yaml(manifest_path)
    current = manifest.get("dependencies", {}).get("apm", [])
    desired = desired_dependencies(args.include_unreleased)
    if current == desired:
        print("Kit atlas-all já está sincronizado")
        return 0
    if args.check:
        print("Kit atlas-all está fora de sincronia")
        return 1

    current_paths = {item.get("path") for item in current if isinstance(item, dict)}
    desired_paths = {item["path"] for item in desired}
    level = "minor" if current_paths != desired_paths else "patch"
    manifest["version"] = bump_semver(str(manifest["version"]), level)
    manifest.setdefault("dependencies", {})["apm"] = desired
    dump_yaml(manifest_path, manifest)

    changelog_path = ROOT / "kits/all/CHANGELOG.md"
    changelog = changelog_path.read_text(encoding="utf-8")
    entries = "\n".join(f"- Inclui `{item['path'].split('/')[-1]}` em `{item['ref']}`." for item in desired)
    release = f"## [{manifest['version']}] - {date.today().isoformat()}\n\n{entries}\n\n"
    heading = "# Changelog\n\n"
    changelog_path.write_text(heading + release + changelog.removeprefix(heading), encoding="utf-8")
    print(f"Kit atlas-all atualizado para {manifest['version']} ({level})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

