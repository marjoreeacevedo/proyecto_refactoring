"""Cliente HTTP compartido por los proveedores (OMDB y TVMaze)."""

import requests
from typing import Optional

from config import CONFIG


def hacer_request(url: str, params: Optional[dict] = None) -> dict:
    """Hace request sin manejo de errores"""
    if CONFIG["debug"]:
        print(f"DEBUG: Haciendo request a {url}")

    response = requests.get(url, params=params, timeout=CONFIG["timeout"])

    if CONFIG["verbose"]:
        print(f"DEBUG: Status code: {response.status_code}")

    return response.json()
