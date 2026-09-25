from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

import yaml


ROOT = Path(__file__).resolve().parents[2]
STATIC_DIR = Path(__file__).resolve().parent / "static"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_BODY_BYTES = 1_000_000
GIT_EXECUTABLE = os.environ.get("APM_MANAGER_GIT", "git")
APM_TYPES = {"squad", "front"}


class ApiError(Exception):
    def __init__(self, status: HTTPStatus, message: str) -> None:
        super().__init__(message)
        self.status = status


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
    except FileNotFoundError as exc:
        raise ApiError(HTTPStatus.NOT_FOUND, f"Arquivo não encontrado: {path.relative_to(ROOT)}") from exc
    if not isinstance(data, dict):
        raise ApiError(HTTPStatus.UNPROCESSABLE_ENTITY, f"YAML inválido: {path.relative_to(ROOT)}")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        yaml.safe_dump(data, stream, allow_unicode=True, sort_keys=False, width=100)


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            [*args],
            cwd=ROOT,
            check=check,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        raise ApiError(HTTPStatus.CONFLICT, f"Comando obrigatório não encontrado: {args[0]}") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or f"Falha ao executar {' '.join(args)}"
        raise ApiError(HTTPStatus.UNPROCESSABLE_ENTITY, message) from exc


def git_available() -> bool:
    try:
        result = run(GIT_EXECUTABLE, "rev-parse", "--is-inside-work-tree", check=False)
    except ApiError:
        return False
    return result.returncode == 0 and result.stdout.strip() == "true"


def current_git_user() -> str:
    if not git_available():
        return os.environ.get("USER", "Usuário do Git")
    result = run(GIT_EXECUTABLE, "config", "user.name", check=False)
    return result.stdout.strip() or os.environ.get("USER", "Usuário do Git")


def git_metadata(path: Path, fallback_author: str) -> tuple[str, str]:
    relative = path.relative_to(ROOT).as_posix()
    if git_available():
        result = run(GIT_EXECUTABLE, "log", "-1", "--format=%an%x1f%aI", "--", relative, check=False)
        if result.returncode == 0 and "\x1f" in result.stdout:
            author, changed_at = result.stdout.strip().split("\x1f", 1)
            return author, changed_at
    changed_at = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()
    return fallback_author, changed_at


def repository_slug(repository: str) -> str:
    parsed = urlparse(repository)
    path = parsed.path.removesuffix(".git").strip("/")
    return path or repository.removesuffix(".git").strip("/")


def skill_catalog() -> list[dict[str, Any]]:
    skills: list[dict[str, Any]] = []
    for manifest_path in sorted(ROOT.glob("skills/*/apm.yml")):
        manifest = load_yaml(manifest_path)
        package_id = manifest_path.parent.name
        catalog_path = manifest_path.parent / "catalog-info.yaml"
        catalog = load_yaml(catalog_path) if catalog_path.exists() else {}
        metadata = catalog.get("metadata", {}) if isinstance(catalog.get("metadata"), dict) else {}
        skills.append(
            {
                "id": package_id,
                "name": str(manifest.get("name", package_id)).replace("-", " ").title(),
                "description": str(metadata.get("description") or manifest.get("description") or ""),
                "version": str(manifest.get("version", "0.0.0")),
                "targets": [str(target) for target in manifest.get("targets", [])],
                "path": manifest_path.parent.relative_to(ROOT).as_posix(),
            }
        )
    return skills


def apm_command(package_dir: Path, manifest: dict[str, Any]) -> str:
    config = load_yaml(ROOT / "atlas.yml")
    name = str(manifest.get("name", package_dir.name))
    version = str(manifest.get("version", "0.0.0"))
    tag_format = str(config.get("tag_format", "{name}--v{version}"))
    tag = tag_format.format(name=name, version=version)
    targets = [str(target) for target in manifest.get("targets", [])]
    default_target = str(config.get("default_target", "kiro"))
    target = default_target if default_target in targets else next(iter(targets), default_target)
    slug = repository_slug(str(config["repository"]))
    relative = package_dir.relative_to(ROOT).as_posix()
    return f"apm install {slug}/{relative}#{tag} --target {target}"


def apm_catalog() -> list[dict[str, Any]]:
    apms: list[dict[str, Any]] = []
    for manifest_path in sorted(ROOT.glob("kits/*/apm.yml")):
        manifest = load_yaml(manifest_path)
        package_dir = manifest_path.parent
        catalog_path = package_dir / "catalog-info.yaml"
        catalog = load_yaml(catalog_path) if catalog_path.exists() else {}
        metadata = catalog.get("metadata", {}) if isinstance(catalog.get("metadata"), dict) else {}
        annotations = metadata.get("annotations", {}) if isinstance(metadata.get("annotations"), dict) else {}
        fallback_author = str(manifest.get("author") or "Núclea Platform AI")
        git_author, updated_at = git_metadata(package_dir, fallback_author)
        dependencies = manifest.get("dependencies", {})
        apm_dependencies = dependencies.get("apm", []) if isinstance(dependencies, dict) else []
        skill_ids = [
            Path(str(item.get("path"))).name
            for item in apm_dependencies
            if isinstance(item, dict) and str(item.get("path", "")).startswith("skills/")
        ]
        apms.append(
            {
                "id": package_dir.name,
                "name": str(manifest.get("name", package_dir.name)),
                "description": str(manifest.get("description") or metadata.get("description") or ""),
                "version": str(manifest.get("version", "0.0.0")),
                "kind": str(annotations.get("atlas.nuclea.io/classification") or ("official" if package_dir.name == "all" else "custom")),
                "type": str(annotations.get("atlas.nuclea.io/apm-type") or ("squad" if package_dir.name == "all" else "front")),
                "segment": str(annotations.get("atlas.nuclea.io/apm-segment") or ("Atlas" if package_dir.name == "all" else "Desenvolvimento web")),
                "author": str(annotations.get("atlas.nuclea.io/last-modified-by") or git_author),
                "requestedBy": str(annotations.get("atlas.nuclea.io/requested-by") or fallback_author),
                "updatedAt": updated_at,
                "targets": [str(target) for target in manifest.get("targets", [])],
                "skillIds": skill_ids,
                "command": apm_command(package_dir, manifest),
            }
        )
    return apms


def full_catalog() -> dict[str, Any]:
    config = load_yaml(ROOT / "atlas.yml")
    return {
        "currentUser": current_git_user(),
        "repositoryUrl": str(config["repository"]).removesuffix(".git"),
        "repositoryReady": git_available(),
        "defaultTarget": str(config.get("default_target", "kiro")),
        "supportedTargets": [str(target) for target in config.get("supported_targets", ["kiro"])],
        "apms": apm_catalog(),
        "skills": skill_catalog(),
    }


def parse_body(handler: SimpleHTTPRequestHandler) -> dict[str, Any]:
    try:
        length = int(handler.headers.get("Content-Length", "0"))
    except ValueError as exc:
        raise ApiError(HTTPStatus.BAD_REQUEST, "Content-Length inválido") from exc
    if length <= 0 or length > MAX_BODY_BYTES:
        raise ApiError(HTTPStatus.BAD_REQUEST, "Corpo da requisição ausente ou muito grande")
    try:
        payload = json.loads(handler.rfile.read(length))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ApiError(HTTPStatus.BAD_REQUEST, "JSON inválido") from exc
    if not isinstance(payload, dict):
        raise ApiError(HTTPStatus.BAD_REQUEST, "O corpo JSON deve ser um objeto")
    return payload


def validate_actor(value: Any) -> str:
    actor = str(value or current_git_user()).strip()
    if not actor or len(actor) > 100 or any(character in actor for character in "\r\n"):
        raise ApiError(HTTPStatus.BAD_REQUEST, "Solicitante inválido")
    return actor


def validate_segment(value: Any) -> str:
    segment = str(value or "").strip()
    if len(segment) < 2 or len(segment) > 60 or any(character in segment for character in "\r\n"):
        raise ApiError(HTTPStatus.BAD_REQUEST, "Informe uma squad ou frente com 2 a 60 caracteres")
    return segment


def validate_skill_ids(value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ApiError(HTTPStatus.BAD_REQUEST, "Selecione ao menos uma skill")
    skill_ids = list(dict.fromkeys(str(item) for item in value))
    available = {item["id"] for item in skill_catalog()}
    unknown = sorted(set(skill_ids) - available)
    if unknown:
        raise ApiError(HTTPStatus.BAD_REQUEST, f"Skills desconhecidas: {', '.join(unknown)}")
    return skill_ids


def validate_targets(value: Any) -> list[str]:
    config = load_yaml(ROOT / "atlas.yml")
    supported = [str(target) for target in config.get("supported_targets", [config.get("default_target", "kiro")])]
    if not isinstance(value, list) or not value:
        raise ApiError(HTTPStatus.BAD_REQUEST, "Selecione ao menos um target")
    targets = list(dict.fromkeys(str(target).strip() for target in value if str(target).strip()))
    unknown = sorted(set(targets) - set(supported))
    if unknown:
        raise ApiError(HTTPStatus.BAD_REQUEST, f"Targets não suportados: {', '.join(unknown)}")
    return targets


def validate_skill_targets(skill_ids: list[str], targets: list[str]) -> None:
    required = set(targets)
    incompatible: list[str] = []
    for skill_id in skill_ids:
        manifest = load_yaml(ROOT / "skills" / skill_id / "apm.yml")
        missing = required - set(str(target) for target in manifest.get("targets", []))
        if missing:
            incompatible.append(f"{skill_id} (falta {', '.join(sorted(missing))})")
    if incompatible:
        raise ApiError(HTTPStatus.BAD_REQUEST, f"Skills incompatíveis com os targets: {'; '.join(incompatible)}")


def dependency_entries(skill_ids: list[str]) -> list[dict[str, str]]:
    config = load_yaml(ROOT / "atlas.yml")
    repository = str(config["repository"])
    tag_format = str(config.get("tag_format", "{name}--v{version}"))
    entries: list[dict[str, str]] = []
    for skill_id in skill_ids:
        manifest = load_yaml(ROOT / "skills" / skill_id / "apm.yml")
        name = str(manifest["name"])
        version = str(manifest["version"])
        entries.append(
            {
                "git": repository,
                "path": f"skills/{skill_id}",
                "ref": tag_format.format(name=name, version=version),
            }
        )
    return entries


def bump_patch(version: str) -> str:
    match = re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", version)
    if not match:
        raise ApiError(HTTPStatus.UNPROCESSABLE_ENTITY, f"Versão SemVer inválida: {version}")
    major, minor, patch = (int(part) for part in match.groups())
    return f"{major}.{minor}.{patch + 1}"


def catalog_document(
    *,
    package_name: str,
    directory_name: str,
    description: str,
    version: str,
    requested_by: str,
    modified_by: str,
    classification: str,
    apm_type: str,
    segment: str,
) -> dict[str, Any]:
    return {
        "apiVersion": "backstage.io/v1alpha1",
        "kind": "Component",
        "metadata": {
            "name": f"atlas-apm-{directory_name}",
            "description": description,
            "annotations": {
                "atlas.nuclea.io/package-path": f"kits/{directory_name}",
                "atlas.nuclea.io/package-version": version,
                "atlas.nuclea.io/requested-by": requested_by,
                "atlas.nuclea.io/last-modified-by": modified_by,
                "atlas.nuclea.io/classification": classification,
                "atlas.nuclea.io/apm-type": apm_type,
                "atlas.nuclea.io/apm-segment": segment,
            },
        },
        "spec": {
            "type": "ai-apm",
            "lifecycle": "production",
            "owner": "group:default/platform-ai",
        },
    }


def require_git_checkout() -> None:
    if not git_available():
        raise ApiError(
            HTTPStatus.CONFLICT,
            "Esta pasta precisa estar conectada a um repositório Git para salvar o APM.",
        )


def validate_repository() -> None:
    run(sys.executable, "tools/validate_repo.py")
    run(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v")


def commit_paths(paths: list[Path], message: str) -> tuple[str, bool, str | None]:
    relative_paths = [path.relative_to(ROOT).as_posix() for path in paths]
    run(GIT_EXECUTABLE, "add", "--", *relative_paths)
    staged = run(GIT_EXECUTABLE, "diff", "--cached", "--quiet", check=False)
    if staged.returncode == 0:
        raise ApiError(HTTPStatus.CONFLICT, "Nenhuma alteração para salvar")
    run(GIT_EXECUTABLE, "commit", "-m", message, "--", *relative_paths)
    commit = run(GIT_EXECUTABLE, "rev-parse", "HEAD").stdout.strip()

    should_push = os.environ.get("APM_MANAGER_PUSH", "1").lower() not in {"0", "false", "no"}
    if not should_push:
        return commit, False, "Commit criado localmente; push desativado por APM_MANAGER_PUSH."

    branch = run(GIT_EXECUTABLE, "branch", "--show-current").stdout.strip()
    if not branch:
        return commit, False, "Commit criado, mas o checkout está em detached HEAD."
    pushed = run(GIT_EXECUTABLE, "push", "origin", f"HEAD:{branch}", check=False)
    if pushed.returncode != 0:
        warning = pushed.stderr.strip() or "Commit criado, mas o push falhou."
        return commit, False, warning
    return commit, True, None


def create_apm(payload: dict[str, Any]) -> dict[str, Any]:
    require_git_checkout()
    name = str(payload.get("name", "")).strip()
    description = str(payload.get("description", "")).strip()
    actor = validate_actor(payload.get("requestedBy"))
    skill_ids = validate_skill_ids(payload.get("skillIds"))
    targets = validate_targets(payload.get("targets"))
    validate_skill_targets(skill_ids, targets)
    apm_type = str(payload.get("apmType", "")).strip()
    segment = validate_segment(payload.get("segment"))

    if not NAME_RE.fullmatch(name) or len(name) > 48:
        raise ApiError(HTTPStatus.BAD_REQUEST, "Nome inválido: use letras minúsculas, números e hífens")
    if len(description) < 8 or len(description) > 160:
        raise ApiError(HTTPStatus.BAD_REQUEST, "A descrição deve ter entre 8 e 160 caracteres")
    if apm_type not in APM_TYPES:
        raise ApiError(HTTPStatus.BAD_REQUEST, "Selecione o tipo Squad ou Frente")

    package_dir = ROOT / "kits" / name
    if package_dir.exists():
        raise ApiError(HTTPStatus.CONFLICT, f"O APM '{name}' já existe")

    version = "1.0.0"
    manifest = {
        "name": name,
        "version": version,
        "description": description,
        "author": actor,
        "license": "UNLICENSED",
        "targets": targets,
        "dependencies": {"apm": dependency_entries(skill_ids)},
    }
    changelog = f"# Changelog\n\n## [{version}] - {date.today().isoformat()}\n\n- Criação do APM com {len(skill_ids)} skill(s).\n"
    paths = [package_dir / "apm.yml", package_dir / "catalog-info.yaml", package_dir / "CHANGELOG.md"]

    try:
        write_yaml(paths[0], manifest)
        write_yaml(
            paths[1],
            catalog_document(
                package_name=name,
                directory_name=name,
                description=description,
                version=version,
                requested_by=actor,
                modified_by=actor,
                classification="custom",
                apm_type=apm_type,
                segment=segment,
            ),
        )
        paths[2].write_text(changelog, encoding="utf-8", newline="\n")
        validate_repository()
        commit, pushed, warning = commit_paths(paths, f"feat(apm): create {name}")
    except Exception:
        if package_dir.exists():
            shutil.rmtree(package_dir)
        raise

    return {"commit": commit, "pushed": pushed, "warning": warning, "apm": name}


def update_apm(directory_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    require_git_checkout()
    if not NAME_RE.fullmatch(directory_name):
        raise ApiError(HTTPStatus.BAD_REQUEST, "Identificador de APM inválido")
    skill_ids = validate_skill_ids(payload.get("skillIds"))
    actor = validate_actor(payload.get("requestedBy"))
    package_dir = ROOT / "kits" / directory_name
    manifest_path = package_dir / "apm.yml"
    catalog_path = package_dir / "catalog-info.yaml"
    changelog_path = package_dir / "CHANGELOG.md"
    if not manifest_path.exists():
        raise ApiError(HTTPStatus.NOT_FOUND, f"APM não encontrado: {directory_name}")

    snapshots = {
        path: path.read_bytes() if path.exists() else None
        for path in (manifest_path, catalog_path, changelog_path)
    }
    manifest = load_yaml(manifest_path)
    targets = [str(target) for target in manifest.get("targets", [])]
    validate_skill_targets(skill_ids, targets)
    current_dependencies = manifest.get("dependencies", {}).get("apm", [])
    new_dependencies = dependency_entries(skill_ids)
    if current_dependencies == new_dependencies:
        raise ApiError(HTTPStatus.CONFLICT, "A composição do APM não foi alterada")

    old_version = str(manifest.get("version", "0.0.0"))
    new_version = bump_patch(old_version)
    manifest["version"] = new_version
    manifest["dependencies"] = {"apm": new_dependencies}
    description = str(manifest.get("description", ""))
    classification = "official" if directory_name == "all" else "custom"
    existing_catalog = load_yaml(catalog_path) if catalog_path.exists() else {}
    existing_metadata = (
        existing_catalog.get("metadata", {}) if isinstance(existing_catalog.get("metadata"), dict) else {}
    )
    existing_annotations = (
        existing_metadata.get("annotations", {})
        if isinstance(existing_metadata.get("annotations"), dict)
        else {}
    )
    requested_by = str(existing_annotations.get("atlas.nuclea.io/requested-by") or actor)
    apm_type = str(existing_annotations.get("atlas.nuclea.io/apm-type") or ("squad" if directory_name == "all" else "front"))
    segment = str(existing_annotations.get("atlas.nuclea.io/apm-segment") or ("Atlas" if directory_name == "all" else "Desenvolvimento web"))
    catalog = catalog_document(
        package_name=str(manifest.get("name", directory_name)),
        directory_name=directory_name,
        description=description,
        version=new_version,
        requested_by=requested_by,
        modified_by=actor,
        classification=classification,
        apm_type=apm_type,
        segment=segment,
    )
    previous_changelog = changelog_path.read_text(encoding="utf-8") if changelog_path.exists() else "# Changelog\n"
    entry = (
        f"\n## [{new_version}] - {date.today().isoformat()}\n\n"
        f"- Atualiza a composição do APM para {len(skill_ids)} skill(s).\n"
    )
    updated_changelog = previous_changelog.rstrip() + "\n" + entry
    paths = [manifest_path, catalog_path, changelog_path]

    try:
        write_yaml(manifest_path, manifest)
        write_yaml(catalog_path, catalog)
        changelog_path.write_text(updated_changelog, encoding="utf-8", newline="\n")
        validate_repository()
        commit, pushed, warning = commit_paths(paths, f"feat(apm): update {manifest['name']} to {new_version}")
    except Exception:
        for path, content in snapshots.items():
            if content is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(content)
        raise

    return {
        "commit": commit,
        "pushed": pushed,
        "warning": warning,
        "apm": str(manifest["name"]),
        "version": new_version,
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        print(f"[{self.log_date_time_string()}] {format % args}")

    def send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def handle_api_error(self, exc: Exception) -> None:
        if isinstance(exc, ApiError):
            self.send_json(exc.status, {"error": str(exc)})
            return
        print(f"Unexpected error: {exc}")
        self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Erro interno ao processar o APM"})

    def do_GET(self) -> None:
        if urlparse(self.path).path == "/api/catalog":
            try:
                self.send_json(HTTPStatus.OK, full_catalog())
            except Exception as exc:
                self.handle_api_error(exc)
            return
        super().do_GET()

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/apms":
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "Rota não encontrada"})
            return
        try:
            result = create_apm(parse_body(self))
            self.send_json(HTTPStatus.CREATED, result)
        except Exception as exc:
            self.handle_api_error(exc)

    def do_PUT(self) -> None:
        path = urlparse(self.path).path
        prefix = "/api/apms/"
        if not path.startswith(prefix):
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "Rota não encontrada"})
            return
        try:
            directory_name = unquote(path.removeprefix(prefix))
            result = update_apm(directory_name, parse_body(self))
            self.send_json(HTTPStatus.OK, result)
        except Exception as exc:
            self.handle_api_error(exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gerenciador web de APMs do Atlas")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"APM Manager disponível em http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
