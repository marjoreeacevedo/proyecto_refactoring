"""Misceláneo: display helpers, tvmaze caché, main entry."""

from unittest.mock import MagicMock, patch

from api import tvmaze
from ui.display import clear_screen, print_header, print_separator
import main as main_mod


def test_separator_y_header(capsys):
    print_separator()
    assert "=" * 60 in capsys.readouterr().out
    print_header("hola")
    assert "HOLA" in capsys.readouterr().out


def test_clear_screen_llama_os():
    with patch("ui.display.os.system") as sistema:
        clear_screen()
    sistema.assert_called_once()


def test_tvmaze_cache_segunda_llamada_sin_red():
    payload = [{"show": {"name": "S"}}]
    respuesta = MagicMock()
    respuesta.status_code = 200
    respuesta.raise_for_status.return_value = None
    respuesta.json.return_value = payload
    with patch("api.client.requests.get", return_value=respuesta) as get:
        assert tvmaze.buscar_series("cacheada") == payload
        assert tvmaze.buscar_series("cacheada") == payload
        assert get.call_count == 1


def test_main_setup_logging_debug_true():
    main_mod.setup_logging()


def test_main_keyboard_interrupt(monkeypatch):
    monkeypatch.setattr("ui.menu.menu_principal", lambda: (_ for _ in ()).throw(KeyboardInterrupt()))
    # main.menu_principal está importado en main; parchear donde se usa
    with patch("main.menu_principal", side_effect=KeyboardInterrupt()):
        try:
            main_mod.main()
        except SystemExit as e:
            assert e.code == 0


def test_main_error_inesperado():
    with patch("main.menu_principal", side_effect=RuntimeError("boom")):
        try:
            main_mod.main()
        except SystemExit as e:
            assert e.code == 1
