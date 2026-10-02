"""Constantes del proyecto (URLs, claves de API y valores por defecto)."""

import os

# Key real vía variable de entorno; sin ella se usa la demo pública.
API_KEY_OMDB: str = os.environ.get("OMDB_API_KEY", "trilogy")  # Demo key
BASE_URL_OMDB: str = "http://www.omdbapi.com/"
BASE_URL_TVMAZE: str = "http://api.tvmaze.com"

DEFAULT_TIMEOUT: int = 30

CACHE_PREFIX_SERIES: str = "series_"
