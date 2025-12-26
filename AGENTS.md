# Repository Guidelines

## Project Structure & Module Organization
- `sqlean/`: SQLean extension stubs 
- `tests/`: Tests.
- `pyproject.toml`: Project configuration.

## Build, Test, and Development Commands
- Install dev deps: `uv sync --all-extras`.
- Run tests directly: `uv run pytest -q` or focused: `uv run pytest -k keyword`.

### Ruff (lint/format)
- Full style pass: `uv run tox -e style` (runs `uv run ruff check --fix` and `uv run ruff format`).
- Direct commands:
  - Lint: `uv run ruff check` (add `--fix` to auto-fix)
  - Format: `uv run ruff format`

## ty (type checking)
- Repo-wide `uv run ty check -v`
- Per-package: `uv run ty check litecli -v`
- Notes:
  - Config is in `pyproject.toml` (target Python 3.9, stricter settings).

## Coding Style & Naming Conventions
- Formatter/linter: Ruff.
- Indentation: 4 spaces. Line length: 140 (see `pyproject.toml`).
- Naming: modules/functions/variables `snake_case`; classes `CamelCase`; tests `test_*.py`.
- Keep imports sorted and unused code removed (ruff enforces).
- Use lowercase type hints for dict, list, tuples etc.
- Use | for Unions and | None for Optional.

## Testing Guidelines
- Framework: Pytest
- Location: place new tests in `tests/` alongside related module area.
- Conventions: name files `test_<unit>.py`; use fixtures from `tests/conftest.py`.
- Quick check: `pytest -q`; coverage report via `tox`.
