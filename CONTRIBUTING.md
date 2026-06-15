# Contributing to EngKey

## How to contribute

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/my-feature`.
3. Make your changes.
4. Run tests: `python3 -m pytest tests/ -v -m "not e2e" --ignore=tests/test_e2e.py`.
5. Run linter: `ruff check .`.
6. Push and open a Pull Request.

## Adding a new translation engine

Create a class in `core/engines.py` that inherits from `BaseEngine` and implements `translate(text, source, target) -> str`. Call `register(YourEngine)` at module level. The engine appears automatically in the Settings UI - no UI changes needed. See `ARCHITECTURE.md` for a complete example.

## Adding a new dialect (Native Mode)

1. Create `core/native/<language>/<dialect_code>.py` with a `process(text) -> str` function.
2. Register it in `core/native/dialects.py`.

## Code style

- Format: `black` (default configuration).
- Lint: `ruff check .` - zero warnings before merging.
- Types: `mypy` on `core/` - all functions must have type annotations.

## Commit messages

Use conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `ci:`.

## Pull Request checklist

- [ ] Tests pass: `python3 -m pytest tests/ -v -m "not e2e"`.
- [ ] Ruff clean: `ruff check .`.
- [ ] New code has tests.
- [ ] Documentation updated if needed.
