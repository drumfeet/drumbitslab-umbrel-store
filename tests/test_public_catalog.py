"""Exercise the publication guard against disposable Git indexes."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


GUARD = Path(__file__).resolve().parents[1] / "scripts/verify-public-catalog.sh"


class PublicCatalogTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="public-catalog-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / "catalog"
        self.repo.mkdir()
        self.env = {
            key: value for key, value in os.environ.items()
            if not key.startswith("GIT_")
        }
        self.env["GIT_CONFIG_NOSYSTEM"] = "1"
        self.git("init", "--quiet")

    def git(self, *arguments):
        return subprocess.run(
            ["git", *arguments], cwd=self.repo, env=self.env,
            check=True, capture_output=True,
        )

    def track(self, *names):
        for name in names:
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("synthetic catalog fixture\n")
        self.git("add", "--force", "--all")

    def guard(self, cwd=None, **environment):
        return subprocess.run(
            ["bash", str(GUARD)], cwd=cwd or self.repo,
            env={**self.env, **environment}, capture_output=True, text=True,
        )

    def test_allows_catalog_sources_and_example_environment_files(self):
        self.track(
            "umbrel-app-store.yml", "app/umbrel-app.yml", "app/docker-compose.yml",
            ".env.example", "app/.env.example", "docs/a file.txt",
            "docs/line\nbreak.txt", "app/database/README.md",
        )
        result = self.guard()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Public catalog check passed.", result.stdout)

    def test_rejects_tracked_runtime_and_environment_files(self):
        for name in (
            ".env", ".env.production", "app/.env.local", "data/state.json",
            "app/local-data/state.json", "artifacts/log.txt",
            "app/screenshots/page.png", "app/data/a file.txt",
            "app/data/line\nbreak.txt",
        ):
            with self.subTest(name=name):
                self.track(name)
                result = self.guard()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(name, result.stderr)
                self.assertNotIn("check passed", result.stdout)
                self.git("rm", "--force", "--", name)

    def test_global_git_ignores_cannot_hide_blocked_fixtures(self):
        for mode in ("configured", "default"):
            with self.subTest(mode=mode):
                home = self.root / mode
                home.mkdir()
                xdg = home / "xdg"
                if mode == "configured":
                    ignore = home / "global-ignore"
                    (home / ".gitconfig").write_text(
                        "[core]\n\texcludesFile = " + str(ignore) + "\n"
                    )
                else:
                    ignore = xdg / "git" / "ignore"
                    ignore.parent.mkdir(parents=True)
                ignore.write_text(".env\n.env.*\n")
                environment = {
                    **os.environ,
                    "HOME": str(home),
                    "XDG_CONFIG_HOME": str(xdg),
                }
                # Select only the rejection cases, avoiding recursive discovery.
                result = subprocess.run(
                    [sys.executable, "-B", str(Path(__file__).resolve()),
                     "PublicCatalogTests.test_rejects_tracked_runtime_and_environment_files", "-v"],
                    cwd=self.repo, env=environment, capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_checks_the_index_without_publishing_untracked_runtime_files(self):
        self.track("README.md")
        (self.repo / ".env").write_text("synthetic untracked fixture\n")
        result = self.guard()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_accepts_an_empty_index(self):
        result = self.guard()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_fails_when_invoked_outside_a_git_repository(self):
        outside = self.root / "outside"
        outside.mkdir()
        result = self.guard(cwd=outside)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("check passed", result.stdout)

    def test_fails_when_git_cannot_read_the_index(self):
        invalid_index = self.root / "invalid-index"
        invalid_index.write_bytes(b"invalid synthetic Git index")
        result = self.guard(GIT_INDEX_FILE=str(invalid_index))
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("check passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
