"""Validación de entradas de usuario (texto, archivos, timeout)."""

import os


def texto_busqueda(valor: str, campo: str, max_largo: int = 200) -> str:
    """Texto sin espacios de más; rechaza vacíos y sobre-largos."""
    limpio = valor.strip()
    if not limpio:
        raise ValueError(f"{campo} no puede estar vacío")
    if len(limpio) > max_largo:
        raise ValueError(f"{campo} demasiado largo (máx. {max_largo})")
    return limpio


def nombre_archivo_seguro(nombre: str) -> str:
    """Nombre sin ruta: rechaza vacío, separadores y '..'."""
    limpio = nombre.strip()
    if not limpio:
        raise ValueError("El nombre de archivo no puede estar vacío")
    if limpio != os.path.basename(limpio) or ".." in limpio:
        raise ValueError(f"Nombre de archivo inválido: {nombre!r}")
    return limpio


def timeout_valido(valor: str) -> int:
    """Entero mayor que cero para el timeout."""
    try:
        numero = int(valor)
    except ValueError:
        raise ValueError("El timeout debe ser un número entero") from None
    if numero <= 0:
        raise ValueError("El timeout debe ser mayor que cero")
    return numero
