"""Punto de entrada: solo lanza el menú principal."""

import sys

from ui.menu import menu_principal


def main() -> None:
    """Ejecuta el programa con control de interrupciones."""
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
