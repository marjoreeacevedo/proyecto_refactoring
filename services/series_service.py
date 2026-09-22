"""Servicio de series: capa fina sobre api.tvmaze (sitio para lógica futura)."""

from api.tvmaze import buscar_series, obtener_detalles_serie

__all__ = [
    "buscar_series",
    "obtener_detalles_serie",
]
