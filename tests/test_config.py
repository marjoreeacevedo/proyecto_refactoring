"""Unitarios de config (get/set con restauración por fixture)."""

from config import CONFIG, get_setting, set_setting


def test_defaults():
    assert CONFIG["debug"] is True
    assert CONFIG["verbose"] is True
    assert CONFIG["timeout"] == 30


def test_get_con_default():
    assert get_setting("timeout") == 30
    assert get_setting("no_existe", "x") == "x"


def test_set_roundtrip():
    set_setting("timeout", 99)
    assert get_setting("timeout") == 99
