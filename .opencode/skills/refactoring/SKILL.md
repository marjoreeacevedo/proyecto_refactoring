---
name: refactoring
description: Use when refactoring Python code with bad practices, globals, wildcard imports, bare except, duplicated code, missing type hints. Use ONLY for code cleanup and SOLID restructuring in proyecto_refactoring.
---

# Refactoring Python

Purpose: identify and remove bad practices without changing expected application behavior.

Derived from root `SKILL.md` (which proposes `skill.json` + `instrucciones.md`, an obsolete format).
This file uses the format recognized by OpenCode 1.18.30: `.opencode/skills/<name>/SKILL.md`
with `name`/`description` frontmatter. Deliverable copy: `opencode/skills/refactoring/SKILL.md`.

## When to act

- Functions too long or with multiple responsibilities, duplicated code, module-level
  globals, `from x import *`, `except:` bare clauses, dead code, unused imports/configs,
  high coupling, mixed UI/business/API logic.

## Procedure

1. **Baseline first:** run `python3 -m pytest -q` before touching code. Record pass/fail.
   Do not start without a green baseline (or a documented failing baseline).
2. **Long functions / SRP:** if a function mixes input + API call + display
   (e.g. old `funcion_buscar_pelicula`), split into `ui/menu.py` (input),
   `services/` (logic), `ui/display.py` (output). One reason to change per function.
3. **Duplicated code:** search with `rg` before extracting helpers. Unify
   (e.g. `any(titulo_de(p) == ...)` instead of repeated `for` loops,
   `len(lista)` instead of manual counters, `for/enumerate` instead of `while i`).
4. **Globals:** `rg -n "^\s*global\s"`. A `global` used only to mutate a dict/list
   (`append`, `CACHE[k] = v`) is unnecessary — remove it. If reassignment remains
   (`HISTORIAL = []`), prefer `lista.clear()` so no `global` is needed. Move shared
   settings to `config.py`, URLs/keys to `constants.py`, or inject via parameters.
5. **Broad except:** `rg -n "except\s*:"`. Replace with
   `except (ValueError, KeyError, requests.RequestException) as e:` or project
   exceptions (`ApiError`, `MovieNotFoundError`, `StorageError`). Never silence with
   `print("error")`; use `logging.getLogger(__name__)` and re-raise or return a typed result.
6. **Dead code:** `rg` for imports of `*_manager.py`, `utils.py`, `logger.py`,
   `legacy_config/`. If zero references, do NOT delete silently — document as candidate
   and ask. Remove only unused imports confirmed by `rg`/linter.
7. **Coupling:** `api/` must not import `services/` or `ui/`. `services/` may call
   `api/` but never `input()/print()`. `ui/` orchestrates only.
8. **Clean code, no over-engineering:** f-strings, explicit imports, basic type hints
   (`str, int, bool, dict, list, None, Optional`). No `Any` to hide missing types,
   no new abstractions (classes, DI frameworks) unless duplication proves need.
9. **Public interfaces:** keep signatures and `__all__` stable
   (`buscar_pelicula`, `agregar_a_favoritas`, etc.). Changing a contract
   (e.g. `None` → exception) requires explicit authorization.
10. **Risks before each group:** state problem, affected files/functions, proposed fix,
    side effects, and how behavior preservation will be checked
    (which `pytest` files + manual smoke test with mocks).
11. **Small batches:** one group at a time, re-run `pytest -q` after each. No massive
    rewrites without justifying every change.

## Do not do

- No mass refactoring without tests before/after.
- No `reset --hard`, no deleting user changes, no contract changes without approval.
- No leaving `*_config.py` unused without documenting it.

## Example

Before:

```python
from api_movies import *
try:
  print("Buscando " + titulo)
  data = buscar(titulo)
except:
  print("error")
```

After:

```python
from api.omdb import buscar_pelicula
import logging
logger = logging.getLogger(__name__)

def funcion_buscar_pelicula(titulo: str) -> None:
    logger.info(f"Buscando {titulo}")
    try:
        pelicula = buscar_pelicula(titulo)
    except (MovieNotFoundError, ApiError) as e:
        print(f"Error: {e}")
        return
```

## Verify

```bash
python3 -m pytest -q
rg -n "except\s*:" api services ui models config.py validators.py main.py
rg -n "^\s*global\s" api services ui
rg -n "import \*" api services ui main.py
```
