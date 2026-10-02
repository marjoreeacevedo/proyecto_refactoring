---
name: api-integration
description: Use when integrating REST APIs in Python with requests, OMDB, TVMaze, cache, retry, rate limiting, timeout, validation.
---

# API Integration Python

Purpose: consume and integrate REST APIs consistently and robustly.

Derived from root `SKILL.md` (obsolete `skill.json` format). This file is the
versioned deliverable (`opencode/skills/api-integration/SKILL.md`), synced with
the active skill at `.opencode/skills/api-integration/SKILL.md`.

## When to act

- New HTTP client, shared config, timeout handling, connection/HTTP/JSON errors,
  duplicate requests, retries, auth/secrets, isolating API deps, mocked tests.

## Procedure

1. **Review current mechanism:** read `api/client.py` (`hacer_request`), `api/omdb.py`,
   `api/tvmaze.py`, `constants.py`, `config.py`. Note who sets timeout, who validates.
2. **Centralize shared config:** base URLs and keys in `constants.py`
   (`BASE_URL_OMDB`, `BASE_URL_TVMAZE`, `API_KEY_OMDB` from `OMDB_API_KEY` env);
   runtime `timeout` in `config.py:CONFIG["timeout"]`. Never hardcode per function.
3. **Timeout always:** every `requests.get(url, params=..., timeout=CONFIG["timeout"])`.
   Never call without `timeout`. Validate user input with `validators.timeout_valido`.
4. **Errors:** catch `requests.RequestException`, raise typed `ApiError` with URL context
   (`raise ApiError(...) from e`). Call `raise_for_status()` before `response.json()`;
   wrap `ValueError` from `.json()` into `ApiError`. Treat `OMDB {"Response":"False"}`
   as `MovieNotFoundError`, not a generic failure.
5. **Validate status + JSON:** check `status_code`, then `data.get(...)` with defaults.
   Never index `data["Title"]` directly. Encode query with `urllib.parse.quote_plus`.
6. **Avoid duplicate requests:** in-memory dict cache per provider
   (`CACHE_PELICULAS`, `CACHE_SERIES` with `CACHE_PREFIX_SERIES`). Cache only successes,
   never errors. Document key policy (exact title vs normalized).
7. **Retries only when safe:** retry `Timeout`/`ConnectionError`/`5xx` only. Never retry
   logic already in a `for intento in range(3)` unless added deliberately.
8. **Limits + backoff when used:** max 3 attempts, `time.sleep(2 ** intento)`. For `429`,
   honor `Retry-After` header. Do not add new retry deps without justification.
9. **No retry of duplicating effects:** GET search/detail may retry; export/import/file
   writes must never auto-retry.
10. **Auth/secrets:** key via `os.environ.get("OMDB_API_KEY", "trilogy")`, template in
    `.env.example`, `.env` git-ignored. Never commit real keys. `rg -n "trilogy|apikey|password"`.
11. **Isolate API deps:** `requests` only inside `api/`. `services/` calls `api/` functions;
    business logic never builds URLs. Keep contracts (`buscar_pelicula -> dict`,
    `buscar_series -> list`) unchanged without approval.
12. **Mocked tests:** `patch("api.client.requests.get")` with `MagicMock`
    (`status_code`, `raise_for_status`, `json`). Cover ok, connection error,
    HTTP 500, invalid JSON, not-found, cache-hit (`assert get.call_count == 1`).
    Never hit OMDB/TVMaze in unit tests.
13. **Document contract per integration:** base URL, params, auth, success shape,
    error mapping, timeout, cache policy. Update `README.md` APIs section.

## Do not do

- No changing existing API contracts or adding deps (`httpx`, `pydantic`, `tenacity`)
  without justifying need.
- No `except:` around network code. No caching errors. No secrets in code/logs.

## Example

```python
import logging, requests
from config import CONFIG
from exceptions.api_error import ApiError
logger = logging.getLogger(__name__)

def hacer_request(url: str, params: dict | None = None) -> dict:
    try:
        r = requests.get(url, params=params, timeout=CONFIG["timeout"])
        r.raise_for_status()
    except requests.RequestException as e:
        raise ApiError(f"Error de red con {url}: {e}") from e
    try:
        return r.json()
    except ValueError as e:
        raise ApiError(f"Respuesta no JSON de {url}: {e}") from e
```

## Verify

```bash
python3 -m pytest tests/test_api.py -q
rg -n "requests\.get" api
rg -n "timeout" api/client.py constants.py config.py
```
