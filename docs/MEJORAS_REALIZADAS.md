# Mejoras realizadas — Proyecto Refactoring (Películas y Series)

Fecha: 2026-10-02. Suite verificada con ejecución real: **74 passed**, cobertura **95 %**.

## 1. Problemas encontrados (análisis inicial)

1. `global` innecesarios en `api/omdb.py:17`, `api/tvmaze.py:13`,
   `services/movie_service.py:65,82,93,99,138`. Solo `limpiar_historial` e
   `importar_de_json` reasignaban; el resto solo mutaba dict/lista.
2. `while i < len(...)` en `ui/display.py:68`, `ui/menu.py:121,178,200`.
3. Duplicación: bucle de existencia en `agregar_a_favoritas`, contadores manuales en
   `obtener_estadisticas`, `range(len())+pop` en `eliminar_de_favoritas`.
4. `tvmaze.py` sin `logging` (inconsistente con `client.py`/`omdb.py`).
5. `*_manager.py` (~22), `utils.py`, `logger.py`, `app.py` monolito y `legacy_config/`
   (~88 archivos) sin ningún import (`rg` 0 referencias). Código muerto aparente.
6. `bare except:` en 0 ocurrencias en código activo (ya corregido en FASE 4).
   Queda solo `except Exception` como catch-all en `main.py:26`, aceptable.
7. API sin reintentos/backoff/rate-limit ni `Session`; caché por título exacto sin
   normalizar; sin validación pydantic (fuera de alcance sin justificar nueva dep).
8. Tests: 54 verdes pero `ui/menu.py` al 16 %, `ui/display.clear_screen` y `main.py`
   sin cubrir; sin `pytest-cov` ni config reproducible.
9. Skills: `SKILL.md` raíz pedía `skill.json` + `instrucciones.md` (obsoleto);
   OpenCode 1.18.30 exige `SKILL.md` con frontmatter. `.gitignore` ignoraba todo
   `.opencode/`, por lo que los skills no se versionaban.

## 2. Cambios realizados

- **Skills:** creados `skills/{refactoring,api-integration,testing}/SKILL.md` y
  sincronizados a `.opencode/skills/*/SKILL.md` (formato OpenCode con frontmatter).
- **Refactor grupo A (`api/`):** eliminados `global CACHE_*`; añadidos hints
  `CACHE_*: dict`, `-> dict/list`; `tvmaze.py` con `logger` + debug de caché.
- **Refactor grupo B (`services/movie_service.py`):** `any()` en favoritas,
  `enumerate` en eliminar, `len()` en stats, `clear()` en limpiar historial,
  `clear()+extend()` en importar (elimina `global` y conserva identidad de lista).
- **Refactor grupo C (`ui/`):** 4 `while` → `for/enumerate`; docstrings aclarados.
- **Tests:** +20 tests (`test_menu_flows.py`, `test_misc.py`); `pytest-cov` en
  `requirements-dev.txt`; `pyproject.toml` con `[tool.pytest]` y `[tool.coverage]`.
- **Docs:** `README.md` ampliado; este documento creado; `.gitignore` ajustado
  (versiona skills, ignora `.coverage`, `.pytest_cache/`, node_modules/locks).

## 3. Archivos modificados

- `api/omdb.py`, `api/tvmaze.py`, `services/movie_service.py`,
  `ui/display.py`, `ui/menu.py`
- `requirements-dev.txt` (+`pytest-cov`), `pyproject.toml` (nuevo),
  `.gitignore`, `README.md`
- Nuevos: `skills/*/SKILL.md` (3), `tests/test_menu_flows.py`, `tests/test_misc.py`,
  `docs/MEJORAS_REALIZADAS.md`
- Sincronizados: `.opencode/skills/*/SKILL.md` (3)

## 4. Justificación de cada cambio relevante

- Quitar `global` sin reasignación: cero riesgo (dict/list mutables); verificado.
- `clear()/extend()` en importar/limpiar: evita `global` y **conserva referencias**
  que `ui/menu.py` y `conftest.py` ya importaron (reasignar las rompía).
- `any()/len()/enumerate`: misma semántica, menos líneas, menos ramas.
- `while→for`: elimina variable índice y off-by-one.
- `logger` en tvmaze: paridad observacional con omdb, sin cambiar salida.
- No se añadió retry/Session/pydantic: habría cambiado comportamiento o añadido
  deps sin justificación (prohibido por la tarea).

## 5. Malas prácticas corregidas

Globals innecesarios, `while i`, conteo manual, bucle de existencia duplicado,
`range(len())`, falta de hints en cachés, logging inconsistente.
`bare except`, wildcard imports, concatenación `+` y secretos ya estaban
corregidos en FASE 2/4/5 — verificado, no re-trabajado.

## 6. Mejoras en integración con APIs

Sin cambio de contrato (exigido). Conservado: cliente central `hacer_request`
con `timeout=CONFIG["timeout"]`, `raise_for_status`, `ApiError` con contexto,
`MovieNotFoundError` para `Response=="False"`, `quote_plus`, caché solo de éxitos,
key por `OMDB_API_KEY` con fallback `trilogy`. Documentado en skill
api-integration + README. Pendiente futuro (no implementado): retries solo para
idempotentes GET con backoff y `Retry-After` — requiere decisión de producto.

## 7. Skills creados y finalidad

| Skill | Path activo | Path entregable | Finalidad |
|---|---|---|---|
| Refactoring | `.opencode/skills/refactoring/SKILL.md` | `skills/refactoring/SKILL.md` | Limpieza sin cambiar comportamiento |
| API Integration | `.opencode/skills/api-integration/SKILL.md` | `skills/api-integration/SKILL.md` | REST robusto con timeouts/errores/caché/mocks |
| Testing | `.opencode/skills/testing/SKILL.md` | `skills/testing/SKILL.md` | pytest + fixtures/mocks/cobertura ≥80 % |

Todos con frontmatter válido (`name` == directorio, `description` 1–1024 chars),
verificado contra https://opencode.ai/docs/skills y `opencode 1.18.30`.

## 8. Pruebas añadidas

- `tests/test_menu_flows.py` (15 tests): buscar película ok/vacía/no-encontrada,
  actor con detalle/sin resultados, series ok/error-red, populares/stats,
  favoritos vacío/con-eliminación, historial vacío/limpiar, export/import ok/error,
  configuración toggles, menú salir/inválida/despacho total.
- `tests/test_misc.py` (6 tests): separator/header, `clear_screen` mockeado,
  tvmaze caché segundo llamado sin red, `setup_logging`, `main` KeyboardInterrupt
  (exit 0) y error inesperado (exit 1).
- Total: 54 → **74 tests**, todos con mocks (`patch(requests.get)`,
  `monkeypatch input`, `tmp_path`), sin red/credenciales/datos reales.

## 9. Resultados reales

```text
74 passed in 2.08s   (python3 -m pytest -q)
```

## 10. Cobertura medida

```text
python3 -m pytest -q --cov=. --cov-report=term-missing
TOTAL 460 stmts, 22 miss → 95 %
api/* 100 %, services/* 100 %, models/* 100 %, validators 100 %,
config/constants/exceptions 100 %, ui/display 100 %, main 94 % (línea 33:
`if __name__ == "__main__"`), ui/menu 90 % (21 líneas: ramas de error
67, 76-79, 93-95, 107-110, 131-133, 155-158, 234-235).
```

Alcance en `pyproject.toml`. Excluidos con justificación: `app.py` (monolito
legacy duplicado), `*_manager.py` + `cache/config_*_v2.py` (0 imports, muertos),
`utils.py`, `logger.py` (0 imports), `legacy_config/` (88 configs archivados),
`docs/`, `tests/`, `opencode/`, `.opencode/`, `skills/`, venv/cachés. Sin esta
exclusión justificada el total era 13 % por ~3357 líneas muertas no probadas.

## 11. Limitaciones / pendientes

- `app.py`, `*_manager.py`, `utils.py`, `logger.py`, `legacy_config/`: candidatos a
  archivar/eliminar, **no eliminados** sin autorización (cambio visible en Git).
- `ui/menu.py` 90 %: faltan ramas de error secundarias (detalle actor no encontrado,
  `obtener_detalles_serie` con `ApiError`, `delay` en opción inválida con red).
- `USUARIO_LOGUEADO = None` y `CONFIG["verbose"]` sin uso: conservados por
  compatibilidad (`__all__`/contrato), documentados como reservados.
- Caché por título exacto (case-sensitive) conservada para no cambiar
  comportamiento; normalizar (`lower().strip()`) es mejora futura con tests.
- `delay(1)` y `os.system(clear)` conservados (comportamiento UI).

## 12. Riesgos y recomendaciones

- `importar` ahora conserva identidad de lista: más seguro, pero si algún código
  externo dependía de reasignación (comparar `id()`), revisar. Tests lo cubren.
- Añadir reintentos a `hacer_request` sin distinguir GET idempotente vs escrituras
  duplicaría efectos; hacerlo solo con límites + backoff + `Retry-After`.
- No commitear `.env`, `*.json` exportados, `.coverage`, `.pytest_cache/`
  (ya ignorados). No hacer `reset --hard` ni commits sin autorización del dueño.
- Próximo paso sugerido: decidir ganador `main.py` vs `app.py`, archivar managers
  muertos en rama separada, y subir `ui/menu.py` al 100 % con 3–4 tests de ramas.
