# MathEqs

AI-powered physics equation explainer. Uses [litellm](https://docs.litellm.ai) to support **any** LLM provider — OpenAI, Gemini, Anthropic, Ollama, and [100+ more](https://docs.litellm.ai/docs/providers).

[![CI](https://github.com/csv610/MathEqs/actions/workflows/ci.yml/badge.svg)](https://github.com/csv610/MathEqs/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)]()
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000)](https://github.com/astral-sh/ruff)
[![Mypy](https://img.shields.io/badge/typing-mypy%20strict-2a5dcf)](https://github.com/python/mypy)

## Quick Start

```bash
pip install -r requirements.txt
# Set ONE of these (pick your provider):
export OPENAI_API_KEY="sk-..."
# or: export GEMINI_API_KEY="..."
# or: export ANTHROPIC_API_KEY="..."

# Run it:
python cli.py "F = ma"
python cli.py list
```

### Using local models (Ollama)

```bash
# Install & run Ollama, then pull a model:
ollama pull gemma4
python cli.py -m ollama/gemma4 explain "E = mc²"
```

## Usage

```bash
python cli.py "Schrödinger's Equation"
python cli.py analyze "E = mc²" -o einstein.md
python cli.py -m gpt-4o explain "F = ma"
python cli.py history "Newton's Second Law"
python cli.py derivation "Wave Equation"
python cli.py explain "F = ma" -o equation.md --seed 42
```

### Difficulty Levels

```bash
python cli.py explain "E = mc²" -d beginner
python cli.py explain "E = mc²" -d advanced
```

### Reproducible Outputs

```bash
python cli.py --seed 42 explain "F = ma"
```

Same seed + model + temperature = same output (if the provider supports it).

## Features

- **explain** — Simple + detailed explanation with real-world examples
- **history** — Discoverer, date, context, citations, competing theories
- **derivation** — Step-by-step mathematical derivation with reasoning
- **analyze** — All four sections at once (Intro, History, Derivation, Applications)
- **Multi-provider** — Switch models with `-m` (OpenAI, Gemini, Claude, Ollama, etc.)
- **Reproducible** — `--seed` flag for deterministic outputs
- **Auto-retry** — Exponential backoff on rate limits and API errors
- **Markdown export** — `-o file.md` saves any command's output
- **Pseudoscience guard** — Warns on known pseudoscientific terms

## Setup

1. Clone and install:
   ```bash
   git clone https://github.com/csv610/MathEqs.git
   cd MathEqs
   python3 -m venv mathenv && source mathenv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env   # then edit with your API key
   ```

2. Set one environment variable for your chosen provider:
   - `OPENAI_API_KEY` for OpenAI (`gpt-4o`, `gpt-4o-mini`)
   - `GEMINI_API_KEY` for Google Gemini (`gemini/gemini-2.5-flash`)
   - `ANTHROPIC_API_KEY` for Anthropic (`claude-3-5-sonnet`)
   - No key needed for local Ollama models

3. Run `python cli.py list` to verify it works.

## Project Structure

```
cli.py                 CLI entry point
equation_explainer.py  Core LLM orchestration (retry, seed, prompts)
models.py              Pydantic schemas (7 models, all extra="forbid")
cli_utils.py           Rich terminal formatting + Markdown export
example.py             Demo script (python example.py)
tests/                 46 tests, 100% coverage on core modules
```

## Dependencies

- `litellm` — Universal LLM API
- `pydantic` — Structured output with `response_format`
- `rich` — Terminal UI
- `python-dotenv` — API key management

## Development

```bash
make lint       # ruff check
make type-check # mypy --strict
make test       # pytest + coverage
```

## License

MIT
