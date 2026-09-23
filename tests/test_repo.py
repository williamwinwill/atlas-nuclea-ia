from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.repo_model import ROOT, bump_semver, discover_packages, load_config, parse_frontmatter, tag_for


class RepositoryContractTests(unittest.TestCase):
    def test_expected_packages_are_discoverable(self) -> None:
        packages = discover_packages()
        self.assertEqual(
            {package.name for package in packages},
            {"atlas-all", "pipeline-review", "sonar-fix", "terraform-review"},
        )

    def test_skill_identity_matches_frontmatter(self) -> None:
        for package in discover_packages():
            if package.kind != "skill":
                continue
            skill_file = package.path / ".apm/skills" / package.name / "SKILL.md"
            frontmatter, _ = parse_frontmatter(skill_file)
            self.assertEqual(frontmatter["name"], package.name)
            self.assertEqual(tag_for(package), f"{package.name}--v{package.version}")

    def test_all_kit_references_every_bootstrap_skill(self) -> None:
        packages = discover_packages()
        kit = next(package for package in packages if package.name == "atlas-all")
        skill_paths = {package.relative_path for package in packages if package.kind == "skill"}
        dependency_paths = {item["path"] for item in kit.manifest["dependencies"]["apm"]}
        self.assertEqual(dependency_paths, skill_paths)

    def test_semver_bumps(self) -> None:
        self.assertEqual(bump_semver("1.2.3", "patch"), "1.2.4")
        self.assertEqual(bump_semver("1.2.3", "minor"), "1.3.0")
        self.assertEqual(bump_semver("1.2.3", "major"), "2.0.0")

    def test_repository_configuration_has_no_placeholder(self) -> None:
        config = load_config()
        self.assertEqual(config["repository"], "https://github.com/nuclea/atlas-nuclea-ia.git")
        self.assertEqual(str(config["apm_version"]), "0.31.0")
        self.assertNotIn("ORG", config["repository"])

    def test_release_metadata_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "metadata.json"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools/release_metadata.py"),
                    "--name",
                    "terraform-review",
                    "--version",
                    "1.0.0",
                    "--path",
                    "skills/terraform-review",
                    "--tag",
                    "terraform-review--v1.0.0",
                    "--sha",
                    "a" * 40,
                    "--repository",
                    "https://github.com/nuclea/atlas-nuclea-ia",
                    "--output",
                    str(output),
                ],
                check=True,
            )
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["schemaVersion"], 1)
            self.assertEqual(payload["sha"], "a" * 40)
            self.assertTrue(payload["releaseUrl"].endswith("terraform-review--v1.0.0"))


if __name__ == "__main__":
    unittest.main()
