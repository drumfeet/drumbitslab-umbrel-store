"""Check the packages an Umbrel device discovers in this store."""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
STORE_ID = "drumfeet"
ATLAS_ID = "drumfeet-atlas-almanac-collector"


def read_yaml(path):
    with path.open(encoding="utf-8") as source:
        return yaml.safe_load(source)


def app_directories():
    return sorted(
        path for path in ROOT.iterdir()
        if path.is_dir() and (
            path.name.startswith(STORE_ID + "-")
            or (path / "umbrel-app.yml").is_file()
            or (path / "docker-compose.yml").is_file()
        )
    )


class CatalogPackagesTests(unittest.TestCase):
    def test_store_keeps_its_registered_identity(self):
        store = read_yaml(ROOT / "umbrel-app-store.yml")
        self.assertEqual(store["id"], STORE_ID)
        self.assertIsInstance(store["name"], str)
        self.assertTrue(store["name"].strip())

    def test_installable_app_manifests_match_their_directory_and_declare_a_release(self):
        apps = app_directories()
        self.assertTrue(apps, "No installable app packages found")
        for app in apps:
            with self.subTest(app=app.name):
                manifest = read_yaml(app / "umbrel-app.yml")
                self.assertTrue(app.name.startswith(STORE_ID + "-"))
                self.assertEqual(manifest["id"], app.name)
                self.assertIs(type(manifest["manifestVersion"]), int)
                self.assertEqual(manifest["manifestVersion"], 1)
                for field in ("name", "version"):
                    self.assertIsInstance(manifest[field], str, field)
                    self.assertTrue(manifest[field].strip(), field)

    def test_installable_services_use_digest_pinned_images(self):
        for app in app_directories():
            with self.subTest(app=app.name):
                services = read_yaml(app / "docker-compose.yml")["services"]
                self.assertTrue(services)
                for name, service in services.items():
                    with self.subTest(service=name):
                        self.assertNotIn("build", service, "Use the published image")
                        # Umbrel supplies the default image for its app proxy.
                        if name == "app_proxy" and "image" not in service:
                            continue
                        self.assertRegex(service["image"], r"\A[^@\s]+@sha256:[0-9a-f]{64}\Z")

    def test_atlas_web_and_data_initializer_use_the_same_catalog_release(self):
        atlas = ROOT / ATLAS_ID
        version = read_yaml(atlas / "umbrel-app.yml")["version"]
        services = read_yaml(atlas / "docker-compose.yml")["services"]
        web_image = services["web"]["image"]
        self.assertTrue(web_image.startswith(f"ghcr.io/drumfeet/atlas-almanac-collector:{version}@sha256:"),
                        "Atlas web must use the published catalog version")
        self.assertEqual(services["data_init"]["image"], web_image)
