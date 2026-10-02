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
| `requirements.txt` | Dependencias (`requests`, `json5`)                  |
| `requirements-dev.txt` | Dependencias de test (`pytest`, `pytest-cov`)   |
| `pyproject.toml` | Config de pytest + coverage (alcance y omits)     |
| `opencode/skills/*/SKILL.md` | Copias versionadas de los 3 skills (entregable) |
| `.opencode/skills/*/SKILL.md` | Skills activos que carga OpenCode 1.18.30 |
| `docs/`   | `documentacion_proyecto_refactoring.pdf` + `MEJORAS_REALIZADAS.md` |

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

## Refactorizado — FASE 5 (seguridad, aplicado y verificado)

- Sin contraseñas en el código (verificado por búsqueda): el único dato sensible era la demo key.
- `OMDB_API_KEY` por variable de entorno con fallback a `"trilogy"`; plantilla en `.env.example` (`.env` ignorado por git).
- `validators.py`: `texto_busqueda` (no vacío, máx. 200), `nombre_archivo_seguro` (sin rutas ni `..`, cierra path traversal en export/import), `timeout_valido` (entero > 0).
- URLs con `urllib.parse.quote_plus` (títulos con espacios, acentos o `&`).
- 17 tests nuevos en `tests/test_validators.py`; suite total 48/48.

## Refactorizado — FASE 6 (calidad, aplicado y verificado)

- Sin `global` innecesarios en `api/omdb.py`, `api/tvmaze.py`, `services/movie_service.py`
  (`clear()`/`extend()` en lugar de reasignar; se conserva la identidad de las listas).
- `while i < len(...)` → `for/enumerate` en `ui/display.py` y `ui/menu.py`.
- Duplicados eliminados: `any()` en favoritas, `len()` en estadísticas,
  `enumerate+pop` en eliminar.
- `tvmaze.py` con `logging.getLogger(__name__)` como `omdb.py`/`client.py`.
- Suite: 74/74 tests (54 previos + 20 nuevos de menú/main/display/caché).
- Cobertura 95 % sobre alcance (`pyproject.toml`), ver `docs/MEJORAS_REALIZADAS.md`.
- Skills OpenCode creados y activos (ver abajo).

## Pendiente (próximas fases)

- `app.py` duplicado de `main.py` + `api_movies.py`: elegir un ganador.
- `bare except:` en `mostrar_pelicula` e importar → usar `.get()` y excepciones concretas.
- Validar red (`hacer_request`), archivos (export/import) y entradas (`int(input)`).
- Bucles `while i` → `for/enumerate`; helper `pausa()` para el texto repetido.
- Tests unitarios.

## APIs utilizadas

- **OMDB API**: demo key `"trilogy"` (pública, sin registro).
- **TVMaze API**: pública, sin key.

## Requisitos e instalación

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Configuración del entorno

| Variable | Uso | Valor sin configurar |
|---|---|---|
| `OMDB_API_KEY` | Key de OMDB usada en `constants.py:API_KEY_OMDB` | `"trilogy"` (demo pública) |

Plantilla en `.env.example` (copiar a `.env`, nunca commiteado; `.env` ignorado por git).
`CONFIG["timeout"]` (defecto `30` en `constants.py:DEFAULT_TIMEOUT`) se puede cambiar
en el menú (opción 11) con validación `validators.timeout_valido`.

## Cómo ejecutar

```bash
python main.py
```

## Cómo ejecutar las pruebas

```bash
# Suite completa (unitarias + integración mockeada)
python3 -m pytest -q

# Solo integración mockeada (red simulada, sin servicios externos)
python3 -m pytest tests/test_api.py -q

# Solo flujos de menú
python3 -m pytest tests/test_menu.py tests/test_menu_flows.py -q
```

Estructura real de tests: `tests/conftest.py` (fixtures `pelicula_omdb`,
`aislar_estado`), `test_api.py`, `test_movie_service.py`, `test_menu.py`,
`test_menu_flows.py`, `test_misc.py` (main/display/caché), `test_models.py`,
`test_display.py`, `test_config.py`, `test_validators.py`.

## Cómo medir la cobertura

```bash
python3 -m pytest -q --cov=. --cov-report=term-missing
```

Configuración reproducible en `pyproject.toml` (`[tool.coverage.run]` con `omit`
justificado para legado muerto: `app.py`, `*_manager.py`, `utils.py`, `logger.py`,
`legacy_config/`, `docs/`, `tests/`, `opencode/`, `.opencode/`).
Alcance medido: `api/`, `services/`, `models/`, `ui/`, `exceptions/`, `config.py`,
`constants.py`, `validators.py`, `main.py`. Resultado actual: **95 %** (ver detalle
por módulo en `docs/MEJORAS_REALIZADAS.md`).

## Skills de OpenCode

Formato reconocido por OpenCode 1.18.30: un directorio por skill con `SKILL.md`
y frontmatter `name:` + `description:` (`name` == nombre del directorio).
El `SKILL.md` de la raíz proponía `skill.json` + `instrucciones.md`, formato
obsoleto que OpenCode ya no carga; se documenta la diferencia y se cumple ambos
requisitos con copias sincronizadas:

| Skill | Activo (carga OpenCode) | Entregable versionado |
|---|---|---|
| Refactoring | `.opencode/skills/refactoring/SKILL.md` | `opencode/skills/refactoring/SKILL.md` |
| API Integration | `.opencode/skills/api-integration/SKILL.md` | `opencode/skills/api-integration/SKILL.md` |
| Testing | `.opencode/skills/testing/SKILL.md` | `opencode/skills/testing/SKILL.md` |

`.gitignore` versiona ambos paths e ignora solo
`.opencode/node_modules/`, `package-lock.json` y `server.lock.json`.

## Resumen de mejoras de calidad

Ver detalle en `docs/MEJORAS_REALIZADAS.md`: sin `global` innecesarios, sin
`while i`, sin `bare except` (ya estaba en 0), cachés solo de éxitos, errores
tipados (`ApiError`, `MovieNotFoundError`, `StorageError`), validación de
entradas, `quote_plus` en URLs, 20 tests nuevos, cobertura 95 %.
