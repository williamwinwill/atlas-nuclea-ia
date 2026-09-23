from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parents[1]
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:[-+][0-9A-Za-z.-]+)?$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class Package:
    path: Path
    kind: str
    name: str
    version: str
    manifest: dict[str, Any]

    @property
    def relative_path(self) -> str:
        return self.path.relative_to(ROOT).as_posix()


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: o YAML raiz deve ser um mapa")
    return data


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        yaml.safe_dump(data, stream, allow_unicode=True, sort_keys=False, width=100)


def load_config() -> dict[str, Any]:
    return load_yaml(ROOT / "atlas.yml")


def discover_packages() -> list[Package]:
    packages: list[Package] = []
    for kind, pattern in (("skill", "skills/*/apm.yml"), ("kit", "kits/*/apm.yml")):
        for manifest_path in sorted(ROOT.glob(pattern)):
            manifest = load_yaml(manifest_path)
            packages.append(
                Package(
                    path=manifest_path.parent,
                    kind=kind,
                    name=str(manifest.get("name", "")),
                    version=str(manifest.get("version", "")),
                    manifest=manifest,
                )
            )
    return packages


def package_for_path(path: str | Path) -> Package:
    candidate = (ROOT / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
    for package in discover_packages():
        if package.path.resolve() == candidate:
            return package
    raise ValueError(f"pacote não encontrado: {path}")


def parse_semver(value: str) -> tuple[int, int, int]:
    match = SEMVER_RE.fullmatch(value)
    if not match:
        raise ValueError(f"SemVer inválido: {value}")
    return tuple(int(part) for part in match.groups()[:3])  # type: ignore[return-value]


def bump_semver(value: str, level: str) -> str:
    major, minor, patch = parse_semver(value)
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    if level == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"nível de incremento inválido: {level}")


def tag_for(package: Package | tuple[str, str]) -> str:
    name, version = (package.name, package.version) if isinstance(package, Package) else package
    return str(load_config()["tag_format"]).format(name=name, version=version)


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def tag_exists(tag: str) -> bool:
    result = run_git("show-ref", "--verify", "--quiet", f"refs/tags/{tag}", check=False)
    return result.returncode == 0


def changed_files(base: str) -> list[str]:
    result = run_git("diff", "--name-only", f"{base}...HEAD")
    return [line for line in result.stdout.splitlines() if line]


def affected_packages(base: str | None = None) -> list[Package]:
    packages = discover_packages()
    if not base:
        return packages
    changed = changed_files(base)
    shared = tuple(str(item) for item in load_config().get("shared_validation_paths", []))
    if any(path == prefix.rstrip("/") or path.startswith(prefix) for path in changed for prefix in shared):
        return packages
    affected: list[Package] = []
    for package in packages:
        prefix = f"{package.relative_path}/"
        if any(path == package.relative_path or path.startswith(prefix) for path in changed):
            affected.append(package)
    return affected


def git_show_yaml(base: str, relative_path: str) -> dict[str, Any] | None:
    result = run_git("show", f"{base}:{relative_path}", check=False)
    if result.returncode != 0:
        return None
    data = yaml.safe_load(result.stdout)
    return data if isinstance(data, dict) else None


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: frontmatter ausente")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError(f"{path}: frontmatter sem fechamento") from exc
    data = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter deve ser um mapa")
    return data, "\n".join(lines[end + 1 :])


def package_matrix(packages: Iterable[Package]) -> str:
    include = [
        {
            "path": package.relative_path,
            "kind": package.kind,
            "name": package.name,
            "version": package.version,
            "tag": tag_for(package),
        }
        for package in packages
    ]
    return json.dumps({"include": include}, separators=(",", ":"), ensure_ascii=False)

