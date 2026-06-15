# Contributing to EngKey

## How to contribute

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/my-feature`.
3. Make your changes.
4. Run tests: `pytest -q`.
5. Run linter: `ruff check .`
6. Push and open a PR.

## Adding a new translation engine

1. Create a class in `core/engines.py` inheriting from `BaseEngine`.
2. Implement `translate(text, source, target) -> str`.
3. Call `register(YourEngine)` at module level.
4. It appears automatically in the Settings UI — zero UI changes needed.

See `COPILOT.md` for the full pattern with a code example.

## Adding a new dialect (Modo Nativo)

1. Create `core/native/<lang>/<dialect_code>.py` with a `process(text) -> str` function.
2. Register it in `core/native/dialects.py`.

## Code style

- Format: `black` (default config).
- Lint: `ruff check .` — zero warnings before merging.
- Types: `mypy` on `core/` — all functions must have type annotations.

## Commit messages

Use conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `ci:`.

## PR checklist

- [ ] Tests pass (`pytest -q`).
- [ ] Ruff clean (`ruff check .`).
- [ ] MyPy clean (`mypy core/`).
- [ ] New code has tests.
- [ ] Docs updated if needed.
