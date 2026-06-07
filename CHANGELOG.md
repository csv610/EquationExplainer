# Changelog

## [1.0.0] - 2026-06-07

### Added
- Initial release of MathEqs: AI-powered physics equation explainer
- CLI with explain, history, derivation, analyze subcommands
- Support for any litellm-compatible LLM provider
- Rich terminal output with formatted panels
- Markdown export for all analysis types
- Comprehensive 7-model pydantic response schema with `extra="forbid"`
- Pre-commit hooks (ruff, mypy, formatting)
- CI with GitHub Actions (lint, mypy, test matrix across Python 3.10–3.13)
- Full test suite with 63 tests and 100% core coverage
- Makefile targets for common dev tasks
