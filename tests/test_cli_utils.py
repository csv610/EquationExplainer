"""Tests for cli_utils"""

from cli_utils import generate_four_section_markdown, generate_markdown_document


class TestGenerateMarkdown:
    def test_generate_markdown_basic(self):
        result = generate_markdown_document(
            title="Test Eq",
            equation="F = ma",
            content_dict={"Intro": "Newton's law"},
        )
        assert "# Test Eq" in result
        assert "$$" in result
        assert "F = ma" in result
        assert "Newton's law" in result

    def test_generate_four_section_markdown(self):
        result = generate_four_section_markdown(
            equation_name="Test Eq",
            equation="E = mc²",
            introduction="Simple intro",
            history="Some history",
            derivation="Step by step",
            applications="Used everywhere",
        )
        assert "# Test Eq" in result
        assert "## Introduction" in result
        assert "## History" in result
        assert "## Derivation" in result
        assert "## Applications" in result

    def test_generate_four_section_skips_empty(self):
        result = generate_four_section_markdown(
            equation_name="Eq",
            equation="x = y",
            introduction="",
            history="Has history",
            derivation="",
            applications="",
        )
        assert "## Introduction" not in result
        assert "## History" in result
        assert "## Derivation" not in result
        assert "## Applications" not in result
