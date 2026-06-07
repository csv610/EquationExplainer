"""Tests for CLI"""
import os
from unittest.mock import patch

from cli import _format_year, _parse_global_flags, create_parser


class TestParseGlobalFlags:
    def test_defaults(self):
        args = _parse_global_flags()
        assert args.difficulty == "intermediate"
        assert args.model is None
        assert args.seed is None

    def test_custom_difficulty(self):
        with patch("sys.argv", ["cli.py", "-d", "beginner", "F = ma"]):
            args = _parse_global_flags()
            assert args.difficulty == "beginner"

    def test_custom_model(self):
        with patch("sys.argv", ["cli.py", "-m", "gpt-4o", "explain", "F = ma"]):
            args = _parse_global_flags()
            assert args.model == "gpt-4o"


class TestFormatYear:
    def test_known_year(self):
        assert _format_year(1687) == "1687"

    def test_none_year(self):
        assert _format_year(None) == "Unknown"


class TestApiKeyCheck:
    def test_no_warning_for_ollama(self):
        with patch("cli.os.environ", {}):
            from cli import _check_api_key
            _check_api_key("ollama/gemma4")

    def test_warning_when_no_keys_set(self, capsys):
        with patch("cli.os.environ", {}):
            from cli import _check_api_key
            _check_api_key("gpt-4o")
            captured = capsys.readouterr()
            assert "No API keys found" in captured.out

    def test_no_warning_when_key_set(self, capsys):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}):
            from cli import _check_api_key
            _check_api_key("gpt-4o")
            captured = capsys.readouterr()
            assert captured.out == ""


class TestCliParser:
    def test_create_parser_explain(self):
        parser = create_parser()
        args = parser.parse_args(["explain", "F = ma"])
        assert args.command == "explain"
        assert args.equation == "F = ma"
        assert args.func is not None

    def test_create_parser_history(self):
        parser = create_parser()
        args = parser.parse_args(["history", "E = mc²"])
        assert args.command == "history"
        assert args.equation_name == "E = mc²"

    def test_create_parser_derivation(self):
        parser = create_parser()
        args = parser.parse_args(["derivation", "Wave Equation"])
        assert args.command == "derivation"
        assert args.equation_name == "Wave Equation"

    def test_create_parser_analyze(self):
        parser = create_parser()
        args = parser.parse_args(["analyze", "F = ma", "-o", "out.md", "-d", "beginner"])
        assert args.command == "analyze"
        assert args.output == "out.md"
        assert args.difficulty == "beginner"

    def test_create_parser_list(self):
        parser = create_parser()
        args = parser.parse_args(["list"])
        assert args.command == "list"

    def test_create_parser_version(self):
        parser = create_parser()
        args = parser.parse_args(["version"])
        assert args.command == "version"

    def test_create_parser_model_flag(self):
        parser = create_parser()
        args = parser.parse_args(["-m", "gpt-4o", "explain", "F = ma"])
        assert args.model == "gpt-4o"

    def test_create_parser_no_args_shows_help(self):
        parser = create_parser()
        args = parser.parse_args([])
        assert args.command is None
