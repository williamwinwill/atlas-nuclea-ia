#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from repo_model import (
    ROOT,
    SHA_RE,
    SKILL_NAME_RE,
    affected_packages,
    discover_packages,
    git_show_yaml,
    load_config,
    load_yaml,
    package_for_path,
    parse_frontmatter,
    parse_semver,
    tag_exists,
    tag_for,
)


BIDI_OR_TAG = re.compile("[\u202a-\u202e\u2066-\u2069\U000e0000-\U000e007f]")
HIGH_CONFIDENCE_SECRET = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{32,}"
)


def error(errors: list[str], path: Path | str, message: str) -> None:
    display = Path(path).relative_to(ROOT) if isinstance(path, Path) and path.is_absolute() else path
    errors.append(f"{display}: {message}")


def validate_common(package: Any, errors: list[str]) -> None:
    manifest = package.manifest
    if package.name != package.path.name and not (package.kind == "kit" and package.path.name == "all"):
        error(errors, package.path / "apm.yml", "name deve coincidir com o diretório do pacote")
    if not SKILL_NAME_RE.fullmatch(package.name):
        error(errors, package.path / "apm.yml", "name deve usar lowercase, números e hífens")
    try:
        parse_semver(package.version)
    except ValueError as exc:
        error(errors, package.path / "apm.yml", str(exc))
    if not str(manifest.get("description", "")).strip():
        error(errors, package.path / "apm.yml", "description é obrigatória")
    targets = manifest.get("targets")
    if targets != [load_config()["default_target"]]:
        error(errors, package.path / "apm.yml", "targets deve fixar somente o target corporativo")
    changelog = package.path / "CHANGELOG.md"
    if not changelog.exists() or f"## [{package.version}]" not in changelog.read_text(encoding="utf-8"):
        error(errors, changelog, f"deve conter uma entrada para {package.version}")


def validate_skill(package: Any, errors: list[str]) -> None:
    expected = f".apm/skills/{package.name}/"
    if package.manifest.get("type") != "skill":
        error(errors, package.path / "apm.yml", "pacote de skill deve declarar type: skill")
    if package.manifest.get("includes") != [expected]:
        error(errors, package.path / "apm.yml", f"includes deve conter somente {expected}")

    skill_file = package.path / expected / "SKILL.md"
    if not skill_file.exists():
        error(errors, skill_file, "arquivo obrigatório ausente")
        return
    try:
        frontmatter, body = parse_frontmatter(skill_file)
    except ValueError as exc:
        error(errors, skill_file, str(exc))
        return
    if frontmatter.get("name") != package.name:
        error(errors, skill_file, "frontmatter.name deve coincidir com o pacote")
    description = str(frontmatter.get("description", ""))
    if not description.startswith(("Use ", "Aplique ")):
        error(errors, skill_file, "description deve iniciar pela intenção: 'Use ...' ou 'Aplique ...'")
    if len(description) > 1024:
        error(errors, skill_file, "description excede 1024 caracteres")
    if len(body.splitlines()) > 500:
        error(errors, skill_file, "corpo excede 500 linhas; mova detalhes para references/")

    cases = package.path / "tests/cases.yml"
    if not cases.exists():
        error(errors, cases, "cenários comportamentais ausentes")
    else:
        data = load_yaml(cases)
        if not isinstance(data.get("cases"), list) or len(data["cases"]) < 2:
            error(errors, cases, "inclua ao menos dois cenários comportamentais")

    catalog_path = package.path / "catalog-info.yaml"
    if not catalog_path.exists():
        error(errors, catalog_path, "cadastro do Atlas ausente")
    else:
        catalog = load_yaml(catalog_path)
        annotations = catalog.get("metadata", {}).get("annotations", {})
        if annotations.get("atlas.nuclea.io/package-path") != package.relative_path:
            error(errors, catalog_path, "package-path diverge do pacote")
        if str(annotations.get("atlas.nuclea.io/package-version")) != package.version:
            error(errors, catalog_path, "package-version diverge do manifest")
        if annotations.get("atlas.nuclea.io/release-tag") != tag_for(package):
            error(errors, catalog_path, "release-tag diverge da convenção")


def validate_kit(package: Any, packages_by_path: dict[str, Any], errors: list[str]) -> None:
    dependencies = package.manifest.get("dependencies", {}).get("apm", [])
    if not isinstance(dependencies, list) or not dependencies:
        error(errors, package.path / "apm.yml", "kit deve declarar dependencies.apm")
        return
    config = load_config()
    seen: set[str] = set()
    for index, dependency in enumerate(dependencies):
        location = f"dependencies.apm[{index}]"
        if not isinstance(dependency, dict):
            error(errors, package.path / "apm.yml", f"{location} deve usar a forma objeto")
            continue
        if dependency.get("git") != config["repository"]:
            error(errors, package.path / "apm.yml", f"{location}.git deve usar o repositório oficial")
        dep_path = str(dependency.get("path", ""))
        if dep_path in seen:
            error(errors, package.path / "apm.yml", f"dependência duplicada: {dep_path}")
        seen.add(dep_path)
        target = packages_by_path.get(dep_path)
        if not target or target.kind != "skill":
            error(errors, package.path / "apm.yml", f"path de skill desconhecido: {dep_path}")
            continue
        ref = str(dependency.get("ref", ""))
        expected_prefix = f"{target.name}--v"
        if not (SHA_RE.fullmatch(ref) or ref.startswith(expected_prefix)):
            error(errors, package.path / "apm.yml", f"ref de {dep_path} deve ser SHA ou tag {expected_prefix}*")
            continue
        if ref.startswith(expected_prefix):
            referenced_version = ref[len(expected_prefix) :]
            try:
                if parse_semver(referenced_version) > parse_semver(target.version):
                    error(errors, package.path / "apm.yml", f"ref {ref} excede a versão do pacote")
            except ValueError:
                error(errors, package.path / "apm.yml", f"ref com versão inválida: {ref}")
            changelog = (target.path / "CHANGELOG.md").read_text(encoding="utf-8")
            if f"## [{referenced_version}]" not in changelog:
                error(errors, package.path / "apm.yml", f"ref {ref} não aparece no changelog da skill")


def validate_security(package: Any, errors: list[str]) -> None:
    for path in package.path.rglob("*"):
        if not path.is_file() or any(part.startswith(".") and part != ".apm" for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if BIDI_OR_TAG.search(text):
            error(errors, path, "contém caractere Unicode de controle bidirecional/tag")
        if HIGH_CONFIDENCE_SECRET.search(text):
            error(errors, path, "possível credencial privada encontrada")


def validate_version_change(package: Any, base: str, errors: list[str]) -> None:
    old = git_show_yaml(base, f"{package.relative_path}/apm.yml")
    if old is None:
        return
    changed = []
    from repo_model import changed_files

    prefix = f"{package.relative_path}/"
    for path in changed_files(base):
        if not path.startswith(prefix):
            continue
        relative = path[len(prefix) :]
        if relative == "apm.yml" or relative.startswith(".apm/"):
            changed.append(relative)
    if not changed:
        return
    old_version = str(old.get("version", ""))
    try:
        if parse_semver(package.version) <= parse_semver(old_version):
            error(errors, package.path / "apm.yml", f"conteúdo publicável mudou; incremente {old_version}")
    except ValueError as exc:
        error(errors, package.path / "apm.yml", str(exc))
    if package.version != old_version and tag_exists(tag_for(package)):
        error(errors, package.path / "apm.yml", f"tag {tag_for(package)} já existe; nunca reutilize uma versão")


def validate_root(errors: list[str]) -> None:
    config = load_config()
    repository = str(config.get("repository", ""))
    if not repository.startswith("https://github.com/") or not repository.endswith(".git"):
        error(errors, ROOT / "atlas.yml", "repository deve ser uma URL Git HTTPS completa")
    try:
        parse_semver(str(config.get("apm_version", "")))
    except ValueError as exc:
        error(errors, ROOT / "atlas.yml", f"apm_version: {exc}")
    policy = load_yaml(ROOT / "policies/apm-policy.yml")
    if policy.get("enforcement") != "block":
        error(errors, ROOT / "policies/apm-policy.yml", "enforcement deve ser block")
    if policy.get("dependencies", {}).get("require_pinned_constraint") is not True:
        error(errors, ROOT / "policies/apm-policy.yml", "refs limitadas devem ser obrigatórias")
    if policy.get("mcp", {}).get("trust_transitive") is not False:
        error(errors, ROOT / "policies/apm-policy.yml", "MCP transitivo não pode ser confiado automaticamente")

    consumer_path = ROOT / "examples/consumer/apm.yml"
    consumer = load_yaml(consumer_path)
    mcp_entries = consumer.get("dependencies", {}).get("mcp", [])
    if not isinstance(mcp_entries, list) or len(mcp_entries) != 1 or not isinstance(mcp_entries[0], dict):
        error(errors, consumer_path, "exemplo deve declarar exatamente um MCP explícito")
    else:
        sonar = mcp_entries[0]
        if sonar.get("name") != "atlas-sonarqube" or sonar.get("registry") is not False:
            error(errors, consumer_path, "MCP Sonar deve ser self-defined e usar o nome aprovado")
        if sonar.get("transport") != "stdio" or sonar.get("command") != "docker":
            error(errors, consumer_path, "piloto do Sonar deve usar Docker/stdio")
        environment = sonar.get("env", {})
        if environment.get("SONARQUBE_TOKEN") != "${SONARQUBE_TOKEN}":
            error(errors, consumer_path, "token deve ser resolvido exclusivamente pelo ambiente")
        if str(environment.get("SONARQUBE_READ_ONLY", "")).lower() != "true":
            error(errors, consumer_path, "SONARQUBE_READ_ONLY deve permanecer true")
        image_args = [str(item) for item in sonar.get("args", []) if "sonarqube-mcp" in str(item)]
        if len(image_args) != 1 or image_args[0].endswith(":latest") or ":" not in image_args[0]:
            error(errors, consumer_path, "imagem do Sonar MCP deve usar uma versão aprovada")


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida o monorepo de pacotes APM")
    parser.add_argument("--base", help="ref Git base para validar incremento de versão")
    parser.add_argument("--package", action="append", help="valida apenas este pacote")
    args = parser.parse_args()

    errors: list[str] = []
    validate_root(errors)
    all_packages = discover_packages()
    by_path = {package.relative_path: package for package in all_packages}
    if args.package:
        packages = [package_for_path(path) for path in args.package]
    else:
        packages = affected_packages(args.base)

    names: set[str] = set()
    for package in all_packages:
        if package.name in names:
            error(errors, package.path / "apm.yml", f"nome de pacote duplicado: {package.name}")
        names.add(package.name)

    for package in packages:
        validate_common(package, errors)
        validate_security(package, errors)
        if package.kind == "skill":
            validate_skill(package, errors)
        else:
            validate_kit(package, by_path, errors)
        if args.base:
            validate_version_change(package, args.base, errors)

    if errors:
        print("Falha de validação:", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1
    print(f"OK: {len(packages)} pacote(s) validados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
