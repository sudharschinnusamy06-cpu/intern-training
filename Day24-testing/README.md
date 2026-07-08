# Day 24 - Testing & Code Quality

## What I learned
- Unit tests (isolated functions) vs integration tests (full HTTP requests via TestClient)
- pytest fixtures + monkeypatch, conftest.py for shared setup
- In-memory SQLite test DB via dependency_overrides — tests never touch real PostgreSQL
- Coverage reporting with pytest-cov
- Linting (ruff) and formatting (black)
- SQLModel quirk: table models don't raise ValidationError on missing fields (unlike plain Pydantic) — defaults to None instead

## What I did
1. Copied Day21 app into Day24-testing, installed pytest/httpx/pytest-cov/ruff/black
2. Configured pyproject.toml for pytest, ruff, black
3. Unit tests for verify_api_key() — correct key passes, wrong key raises 401
4. Unit tests for Task model — valid data works, missing title defaults to None
5. Built conftest.py — TestClient + in-memory SQLite fixture, overriding real DB dependency
6. Integration tests — full CRUD (create, get all, get one, update, delete) + 404 not-found cases
7. Integration tests — auth (missing key = 422, wrong key = 401)
8. Reviewed coverage report, added tests to close gaps
9. Ran ruff (fixed unused imports/vars, == True/False comparisons) and black (reformatted all files)
10. This README

## Results
- 14/14 tests passing
- 95% coverage (auth.py, models.py, routers/tasks.py at 100%)
- ruff: all checks passed | black: all files formatted

## Known issues (not fixed today)
- `@app.on_event("startup")` deprecated — should use lifespan handlers later
- httpx deprecation warning with TestClient — library-level, not urgent

## Key commands
| Command | Purpose |
|---|---|
| `pytest tests/ -v` | Run all tests |
| `pytest --cov=app --cov-report=term-missing` | Coverage report |
| `ruff check . --fix` | Lint + auto-fix |
| `black .` | Format code |