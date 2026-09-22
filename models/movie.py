"""Helpers de forma para dicts de películas (formato OMDB vs local)."""


def titulo_de(pelicula: dict) -> str:
    """Título en cualquiera de los dos formatos."""
    return str(pelicula.get("Title", pelicula.get("titulo", "")))


def es_formato_omdb(pelicula: dict) -> bool:
    """True si es el formato de la API OMDB."""
    return "Title" in pelicula


def es_formato_local(pelicula: dict) -> bool:
    """True si es el formato local {titulo, anio, rating}."""
    return "titulo" in pelicula


def nueva_entrada_historial(pelicula: dict) -> dict:
    """Entrada de historial para una película."""
    return {
        "titulo": pelicula.get("Title", ""),
        "fecha": "hoy"  # Hardcoded
    }
