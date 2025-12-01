# Equation Explainer

A physics equation explainer CLI application that uses AI to provide detailed explanations of physics equations. Built with Python and powered by Google's Gemini 2.5 Flash model.

## Features

- **Equation Analysis**: Get detailed explanations of physics equations
- **Multiple Explanation Levels**: Simple to advanced difficulty levels
- **Context-Aware**: Provide context to get more relevant explanations
- **Markdown Export**: Save explanations as formatted markdown documents
- **Rich Terminal Output**: Beautiful formatted output in the terminal

## Installation

1. Clone the repository:
```bash
git clone https://github.com/csv610/EquationExplainer.git
cd EquationExplainer
```

2. Create a virtual environment:
```bash
python3 -m venv mathenv
source mathenv/bin/activate  # On Windows: mathenv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your API key:
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

## Usage

The application provides a CLI interface for explaining physics equations.

### Basic Example

```bash
python cli.py explain "E=mc²" --name "Einstein's Mass-Energy Equivalence"
```

### With Context

```bash
python cli.py explain "F=ma" --name "Newton's Second Law" --context "Forces in a car collision"
```

### Difficulty Levels

Control the complexity of explanations:

```bash
python cli.py explain "E=hf" --difficulty beginner
python cli.py explain "E=hf" --difficulty intermediate
python cli.py explain "E=hf" --difficulty advanced
```

### Export to Markdown

Save explanations to a file:

```bash
python cli.py explain "v=u+at" --markdown output.md
```

## Project Structure

- `cli.py` - Main CLI interface and command handlers
- `equation_explainer.py` - Core explainer logic using Gemini API
- `models.py` - Data models for requests and responses
- `cli_utils.py` - Utility functions for formatting and output
- `requirements.txt` - Python dependencies
- `tests/` - Unit tests
- `.gitignore` - Git ignore rules for Python projects

## Dependencies

- `rich` - Beautiful terminal formatting
- `litellm` - LLM API abstraction
- `google-generativeai` - Google Gemini API access

## Requirements

- Python 3.8+
- Google API key for Gemini access

## Development

Run tests:
```bash
make test
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
