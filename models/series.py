"""Helpers de forma para dicts de series (TVMaze)."""


def nombre_show(show: dict) -> str:
    """Nombre del show."""
    return str(show.get("name", ""))


def resumen_corto(show: dict, largo: int = 200) -> str:
    """Resumen recortado con puntos suspensivos."""
    return f"{show.get('summary', 'N/A')[:largo]}..."
