# Proyecto Refactoring — Películas y Series

App de consola que busca películas (OMDB) y series (TVMaze), guarda favoritas e
historial, y exporta/importa a JSON. Proyecto educativo: partió con malas
prácticas intencionales y se está refactorizando por fases, con cambios
pequeños y fáciles de entender.

## Estructura (núcleo)

| Archivo   | Rol                                                        |
| --------- | ---------------------------------------------------------- |
| `main.py` | Menú en consola e interfaz con el usuario                  |
| `api_movies.py` | Llamadas a OMDB/TVMaze, favoritas, historial, caché  |
| `config.py` | Ajustes compartidos (`debug`, `verbose`, `timeout`)      |
| `constants.py` | Valores fijos (URLs, API key demo, timeout por defecto) |
| `requirements.txt` | Dependencias (`requests`)                           |
| `docs/`   | Documentación del análisis y del plan (PDF)                |

## Refactorizado — FASE 2 (aplicado y verificado)

- `config.py` central reemplaza los 88 `*_config.py` (archivados en `legacy_config/`, fuera de este repo).
- `constants.py` reúne URLs, API key y defaults (se eliminaron `API_KEY_TMDB`/`BASE_URL_TMDB`, muertas).
- Sin `from api_movies import *`: `main.py` usa imports explícitos.
- 48 concatenaciones convertidas a f-strings.
- 31 funciones con type hints básicos (`str, int, bool, dict, list, None, Optional`).
- Sin cambios de comportamiento: verificado con prueba de humo (config compartida, favoritas, export/import JSON).

## Pendiente (próximas fases)

- `app.py` duplicado de `main.py` + `api_movies.py`: elegir un ganador.
- `bare except:` en `mostrar_pelicula` e importar → usar `.get()` y excepciones concretas.
- Validar red (`hacer_request`), archivos (export/import) y entradas (`int(input)`).
- Bucles `while i` → `for/enumerate`; helper `pausa()` para el texto repetido.
- Tests unitarios.

## APIs utilizadas

- **OMDB API**: demo key `"trilogy"` (pública, sin registro).
- **TVMaze API**: pública, sin key.

## Cómo ejecutar

```bash
pip install -r requirements.txt
python main.py
```
