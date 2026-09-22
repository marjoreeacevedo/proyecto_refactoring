"""Cliente HTTP compartido por los proveedores (OMDB y TVMaze)."""

import logging
import requests
from typing import Optional

from config import CONFIG
from exceptions.api_error import ApiError

logger = logging.getLogger(__name__)


def hacer_request(url: str, params: Optional[dict] = None) -> dict:
    """Pide JSON a una URL; lanza ApiError si la red o la respuesta fallan."""
    logger.debug("Haciendo request a %s", url)

    try:
        response = requests.get(url, params=params, timeout=CONFIG["timeout"])
        response.raise_for_status()
    except requests.RequestException as e:
        raise ApiError(f"Error de red con {url}: {e}") from e

    logger.debug("Status code: %s", response.status_code)

    try:
        return response.json()
    except ValueError as e:
        raise ApiError(f"Respuesta no JSON de {url}: {e}") from e
