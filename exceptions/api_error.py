"""Fallo de red o respuesta inválida de OMDB/TVMaze."""


class ApiError(Exception):
    """La API no respondió o devolvió algo inesperado."""
