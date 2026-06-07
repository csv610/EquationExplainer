# Contributing

## Setup

```bash
make venv       # Create virtual environment
source mathenv/bin/activate
make install    # Install dependencies
make setup      # Copy .env.example → .env (add your API key)
```

## Development

```bash
make lint       # ruff check
make format     # ruff format
make type-check # mypy strict
make test       # pytest with coverage
```

## Guidelines

- All pydantic models must use `model_config = {"extra": "forbid"}`.
- Response models should not duplicate fields already in `EquationModel`.
- Use `logging.getLogger(__name__)` for all logging; avoid bare `print()`.
- Every public function must have type annotations.
- New features require tests.
