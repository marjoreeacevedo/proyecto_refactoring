"""Configuracion central del proyecto.

Reemplaza en la practica a los 88 modulos *_config.py archivados en
legacy_config/, que no eran importados por ningun modulo en uso.
"""

from constants import DEFAULT_TIMEOUT

CONFIG: dict = {
    "debug": True,
    "verbose": True,
    "timeout": DEFAULT_TIMEOUT,
}


def get_setting(key: str, default=None):
    """Obtiene un valor de configuracion."""
    return CONFIG.get(key, default)


def set_setting(key: str, value) -> None:
    """Establece un valor de configuracion."""
    CONFIG[key] = value
