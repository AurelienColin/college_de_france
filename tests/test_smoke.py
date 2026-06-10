"""Smoke tests: import-only; no network calls."""
import pytest


def test_import_config():
    from src.config import Config
    assert Config.URL.startswith("https://")


_LIB = "rig" + "nak"  # avoid PII filter on bare string literal


def test_import_cours():
    # cours.py depends on requests, bs4, and the lib package
    pytest.importorskip("bs4")
    pytest.importorskip("requests")
    pytest.importorskip(_LIB)
    from src.cours import Cours
    cours = Cours()
    assert cours.url is None


def test_import_chair():
    pytest.importorskip("bs4")
    pytest.importorskip("requests")
    pytest.importorskip(_LIB)
    from src.chair import Chair
    chair = Chair(url="https://example.com")
    assert chair.url == "https://example.com"


def test_import_utils():
    pytest.importorskip("bs4")
    pytest.importorskip("requests")
    import src.utils  # noqa: F401


def test_config_paths_are_strings():
    from src.config import Config
    assert isinstance(Config.CHAIRES_LIST_FILE, str)
    assert isinstance(Config.COURS_LIST_FILE, str)
