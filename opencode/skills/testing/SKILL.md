---
name: testing
description: Use when creating automated tests with pytest, fixtures, mocks, parametrize, coverage, AAA pattern, integration tests for OMDB TVMaze.
---

# Testing con Pytest

Purpose: automated tests with pytest, targeting ≥80% coverage of in-scope app code.

Derived from root `SKILL.md` (obsolete `skill.json` format). This file is the
versioned deliverable (`opencode/skills/testing/SKILL.md`), synced with
the active skill at `.opencode/skills/testing/SKILL.md`.

## When to act

- New service/component, API integration, bug fix needing regression test, coverage <80%.

## Procedure

1. **Identify units:** `services/movie_service.py` (favoritas/historial/stats/export-import),
   `api/client.py` + `api/omdb.py` + `api/tvmaze.py`, `models/`, `validators.py`,
   `ui/display.py`, `ui/menu.py` orchestration. One test file per module.
2. **Unit tests per service:** success, invalid input, errors, edge cases. Follow
   `tests/test_movie_service.py` pattern (uses `pelicula_omdb` fixture, `tmp_path` for files).
3. **Integration tests for connected components:** endpoints/menu flows and service↔API
   with network mocked (`patch("api.client.requests.get")`). Real network never required;
   `tests/test_api.py` is the model (mocked integration, cache-hit asserts).
4. **Fixtures:** reuse `tests/conftest.py` (`pelicula_omdb`, autouse `aislar_estado` that
   restores favoritas/historial/cachés/timeout). Add new fixtures there, not inline dicts.
5. **Mocks:** `unittest.mock.patch/MagicMock` for `requests.get`; `mocker`/`monkeypatch`
   for `input()` in menu tests. Assert call counts for cache (`call_count == 1`).
6. **Cover:** happy path, `ValueError` (validators), `MovieNotFoundError`,
   `ApiError` (network/HTTP/bad JSON), `StorageError` (missing/corrupt/invalid-shape JSON),
   empty lists, duplicates, boundary (200-char text, timeout 0/negativo, `..` paths).
7. **No external deps:** no real OMDB/TVMaze, no real credentials, no production data.
   Files only under `tmp_path`. Tests independent — order must not matter
   (rely on `aislar_estado`).
8. **Reproducible:** `python3 -m pytest -q` green on clean checkout. One logical assert
   per test except `parametrize`. AAA pattern (Arrange-Act-Assert).
9. **Coverage:** `python3 -m pytest -q --cov=. --cov-report=term-missing`
   (config in `pyproject.toml`). In-scope: `api/`, `services/`, `models/`, `ui/`,
   `exceptions/`, `config.py`, `constants.py`, `validators.py`, `main.py`.
   Out of scope (justified, dead/legacy): `app.py`, `*_manager.py`, `utils.py`,
   `logger.py`, `legacy_config/`, `docs/`, `tests/`, `opencode/`, `.opencode/`.
   Never shrink scope artificially to hit 80% — every exclusion must be justified here.
10. **Uncovered gaps:** read `term-missing` `Missing` column per module, add tests for
    those lines (especially `ui/menu.py` branches and `ui/display.py:clear_screen`).
11. **No tautological tests:** assert behavior (`agregar duplicado is False`,
    `raises(StorageError)`), not internals (`_cache` exact dict object, private calls).

## Do not do

- No `try/except` inside tests to hide failures — use `pytest.raises`.
- No order-dependent globals, no real network, no narrowing `--cov` to tested files only.

## Commands (real for this repo)

```bash
python3 -m pytest -q
python3 -m pytest tests/test_api.py -q
python3 -m pytest -q --cov=. --cov-report=term-missing
python3 -m pytest -q --cov=api --cov=services --cov=models --cov=ui --cov=config --cov=constants --cov=validators --cov=main --cov=exceptions --cov-report=term-missing
```

## Verify

- Total / passed / failed from `pytest -q` output.
- Global % + per-module table from coverage report.
- List of still-missing lines to document in `docs/MEJORAS_REALIZADAS.md`.
