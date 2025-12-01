"""Tests for PhysicsEquationExplainer"""
import pytest
import json
from unittest.mock import patch, MagicMock
from equation_explainer import PhysicsEquationExplainer
from models import EquationModel, EquationExplanation


class TestPhysicsEquationExplainer:
    """Tests for PhysicsEquationExplainer class"""

    def test_init(self):
        """Test initializing explainer"""
        explainer = PhysicsEquationExplainer()
        assert explainer.model == "gemini/gemini-2.5-flash"

    def test_build_prompt_basic(self):
        """Test basic prompt building with EquationModel"""
        explainer = PhysicsEquationExplainer()
        equation = EquationModel(
            name="Newton's Second Law",
            equation="F = ma"
        )
        prompt = explainer._build_prompt(equation)

        assert "F = ma" in prompt
        assert "Newton's Second Law" in prompt
        assert "JSON" in prompt or "json" in prompt.lower()

    def test_build_prompt_with_context(self):
        """Test prompt building with context"""
        explainer = PhysicsEquationExplainer()
        equation = EquationModel(
            name="Newton's Second Law",
            equation="F = ma",
            context="Classical mechanics"
        )
        prompt = explainer._build_prompt(equation)

        assert "F = ma" in prompt
        assert "Newton's Second Law" in prompt
        assert "Classical mechanics" in prompt

    def test_build_prompt_includes_schema(self):
        """Test that prompt includes the response model schema"""
        explainer = PhysicsEquationExplainer()
        equation = EquationModel(
            name="Test Equation",
            equation="E = mc²"
        )
        prompt = explainer._build_prompt(equation)

        # Should include schema fields from EquationExplanation
        assert "simple_explanation" in prompt
        assert "detailed_explanation" in prompt
        assert "real_world_example" in prompt
        assert "key_concepts" in prompt

    @patch('litellm.completion')
    def test_explain_equation(self, mock_completion):
        """Test the full explain_equation flow"""
        # Mock the LLM response with parsed Pydantic model
        mock_response = MagicMock()
        mock_explanation = EquationExplanation(
            equation_name="Newton's Second Law",
            equation="F = ma",
            simple_explanation="Simple explanation",
            detailed_explanation="Detailed explanation",
            real_world_example="Real world example",
            key_concepts=["force", "mass", "acceleration"]
        )
        mock_response.choices[0].message.parsed = mock_explanation
        mock_completion.return_value = mock_response

        explainer = PhysicsEquationExplainer()
        equation = EquationModel(
            name="Newton's Second Law",
            equation="F = ma"
        )

        explanation = explainer.explain_equation(equation)

        assert isinstance(explanation, EquationExplanation)
        assert explanation.equation_name == "Newton's Second Law"
        assert explanation.equation == "F = ma"
        assert explanation.simple_explanation == "Simple explanation"
        assert len(explanation.key_concepts) == 3

    @patch('litellm.completion')
    def test_explain_equation_uses_correct_model(self, mock_completion):
        """Test that explain_equation calls the correct model"""
        mock_response = MagicMock()
        mock_explanation = EquationExplanation(
            equation_name="Test",
            equation="E = mc²",
            simple_explanation="Test",
            detailed_explanation="Test",
            real_world_example="Test",
            key_concepts=[]
        )
        mock_response.choices[0].message.parsed = mock_explanation
        mock_completion.return_value = mock_response

        explainer = PhysicsEquationExplainer()
        equation = EquationModel(name="Test", equation="E = mc²")
        explainer.explain_equation(equation)

        # Verify litellm.completion was called with correct model
        mock_completion.assert_called_once()
        call_args = mock_completion.call_args
        assert call_args[1]['model'] == "gemini/gemini-2.5-flash"

    @patch('litellm.completion')
    def test_explain_equation_uses_response_format(self, mock_completion):
        """Test that explain_equation passes EquationExplanation as response_format"""
        mock_response = MagicMock()
        mock_explanation = EquationExplanation(
            equation_name="Test",
            equation="F = ma",
            simple_explanation="Test",
            detailed_explanation="Test",
            real_world_example="Test",
            key_concepts=[]
        )
        mock_response.choices[0].message.parsed = mock_explanation
        mock_completion.return_value = mock_response

        explainer = PhysicsEquationExplainer()
        equation = EquationModel(name="Test", equation="F = ma")
        explainer.explain_equation(equation)

        # Verify response_format is set to EquationExplanation
        call_args = mock_completion.call_args
        assert call_args[1]['response_format'] == EquationExplanation

    @patch('litellm.completion')
    def test_explain_heat_conduction_equation(self, mock_completion):
        """Test explaining Fourier's Heat Conduction equation"""
        mock_response = MagicMock()
        mock_explanation = EquationExplanation(
            equation_name="Fourier's Law of Heat Conduction",
            equation="Q/t = -kA(dT/dx)",
            simple_explanation="Heat flows from hot to cold regions.",
            detailed_explanation="Fourier's law describes heat transfer: Q/t = -kA(dT/dx)",
            real_world_example="Heat flowing through a metal rod",
            key_concepts=["thermal conductivity", "temperature gradient", "heat flux", "Fourier's law"]
        )
        mock_response.choices[0].message.parsed = mock_explanation
        mock_completion.return_value = mock_response

        explainer = PhysicsEquationExplainer()
        equation = EquationModel(
            name="Fourier's Law of Heat Conduction",
            equation="Q/t = -kA(dT/dx)",
            context="Thermodynamics and heat transfer"
        )

        explanation = explainer.explain_equation(equation)

        assert isinstance(explanation, EquationExplanation)
        assert explanation.equation_name == "Fourier's Law of Heat Conduction"
        assert explanation.equation == "Q/t = -kA(dT/dx)"
        assert "heat" in explanation.simple_explanation.lower()
        assert "thermal conductivity" in explanation.key_concepts
        assert len(explanation.key_concepts) == 4

    def test_get_available_equations(self):
        """Test getting list of available equations"""
        explainer = PhysicsEquationExplainer()
        equations = explainer.get_available_equations()

        assert isinstance(equations, list)
        assert len(equations) > 0
        assert "Newton's Second Law" in equations
        assert "Einstein's Mass-Energy Equivalence" in equations
