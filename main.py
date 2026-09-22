"""Punto de entrada: solo lanza el menú principal."""

import logging
import sys

from config import CONFIG
from ui.menu import menu_principal


def setup_logging() -> None:
    """Configura logging según CONFIG (DEBUG si debug activo)."""
    logging.basicConfig(
        level=logging.DEBUG if CONFIG["debug"] else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )


def main() -> None:
    """Ejecuta el programa con control de interrupciones."""
    setup_logging()
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido")
        sys.exit(0)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)


# Programa principal
if __name__ == "__main__":
    main()
