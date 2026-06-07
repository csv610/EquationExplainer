"""Tests for CLI"""

from cli import create_parser


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
