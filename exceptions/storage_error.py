"""Fallo guardando o cargando el JSON local."""


class StorageError(Exception):
    """No se pudo leer/escribir el archivo o su contenido es inválido."""
