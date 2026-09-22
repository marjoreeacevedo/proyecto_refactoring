# Proyecto Refactoring — Películas y Series

App de consola que busca películas (OMDB) y series (TVMaze), guarda favoritas e
historial, y exporta/importa a JSON. Proyecto educativo: partió con malas
prácticas intencionales y se está refactorizando por fases, con cambios
pequeños y fáciles de entender.

## Estructura (núcleo)

| Archivo   | Rol                                                        |
| --------- | ---------------------------------------------------------- |
| `main.py` | Punto de entrada (solo lanza el menú)                      |
| `ui/menu.py` | Orquestación: input → servicio → display                |
| `ui/display.py` | Todo lo que pinta en pantalla                        |
| `services/movie_service.py` | Favoritas, historial, stats, export/import   |
| `services/series_service.py` | Capa fina sobre TVMaze                        |
| `api/omdb.py`, `api/tvmaze.py` | Llamadas HTTP por proveedor + cachés       |
| `api/client.py` | Cliente HTTP compartido (`hacer_request`)              |
| `models/movie.py`, `models/series.py` | Helpers de forma de dicts            |
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

## Refactorizado — FASE 4 (manejo de errores, aplicado y verificado)

- `exceptions/` con `ApiError`, `MovieNotFoundError`, `StorageError` (un archivo por excepción + `__init__`).
- Cero `bare except`: `mostrar_pelicula` usa `.get(..., 'N/A')`; importar/exportar/red capturan excepciones concretas con mensaje.
- `logging` con `logging.getLogger(__name__)` por módulo; nivel atado a `CONFIG["debug"]` (también al cambiarlo en el menú). Fuera los `print("DEBUG: ...")`; los `print()` de interfaz se quedan.
- Contratos nuevos: `buscar_pelicula` lanza `MovieNotFoundError` (antes `None`); `hacer_request` valida status y JSON (`ApiError`); export/import lanzan `StorageError` (incluye JSON corrupto o con forma inválida).
- Verificado con mocks, sin red: red caída, JSON inválido, película inexistente, archivo faltante/corrupto.

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
