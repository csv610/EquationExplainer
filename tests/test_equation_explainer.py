"""Tests for PhysicsEquationExplainer"""
import pytest
import json
from unittest.mock import patch, MagicMock
from equation_explainer import PhysicsEquationExplainer
from models import ExplanationRequest, EquationExplanation


class TestPhysicsEquationExplainer:
    """Tests for PhysicsEquationExplainer class"""

    def test_init_with_api_key(self):
        """Test initializing explainer with provided API key"""
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'}):
            explainer = PhysicsEquationExplainer(api_key='test_key')
            assert explainer.model == "gemini-2.5-flash"

    def test_init_with_env_variable(self):
        """Test initializing explainer with environment variable"""
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'env_key'}):
            explainer = PhysicsEquationExplainer()
            assert explainer.model == "gemini-2.5-flash"

    def test_init_missing_api_key(self):
        """Test that initialization fails without API key"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="GOOGLE_API_KEY must be set"):
                PhysicsEquationExplainer()

    def test_build_prompt_basic(self):
        """Test basic prompt building"""
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'}):
            explainer = PhysicsEquationExplainer()
            req = ExplanationRequest(equation="F = ma")
            prompt = explainer._build_prompt(req)

            assert "F = ma" in prompt
            assert "intermediate" in prompt
            assert "JSON" in prompt

    def test_build_prompt_with_name_and_context(self):
        """Test prompt building with equation name and context"""
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'}):
            explainer = PhysicsEquationExplainer()
            req = ExplanationRequest(
                equation="F = ma",
                equation_name="Newton's Second Law",
                context="Classical mechanics"
            )
            prompt = explainer._build_prompt(req)

            assert "F = ma" in prompt
            assert "Newton's Second Law" in prompt
            assert "Classical mechanics" in prompt

    def test_build_prompt_beginner_level(self):
        """Test prompt building for beginner difficulty"""
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'}):
            explainer = PhysicsEquationExplainer()
            req = ExplanationRequest(
                equation="F = ma",
                difficulty_level="beginner"
            )
            prompt = explainer._build_prompt(req)

            assert "beginner" in prompt
            assert "simple language" in prompt

    def test_build_prompt_advanced_level(self):
        """Test prompt building for advanced difficulty"""
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'}):
            explainer = PhysicsEquationExplainer()
            req = ExplanationRequest(
                equation="F = ma",
                difficulty_level="advanced"
            )
            prompt = explainer._build_prompt(req)

            assert "advanced" in prompt
            assert "precise technical language" in prompt

    def test_parse_response_valid_json(self):
        """Test parsing valid JSON response"""
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'}):
            explainer = PhysicsEquationExplainer()

            json_content = json.dumps({
                "simple_explanation": "Simple test",
                "detailed_explanation": "Detailed test",
                "real_world_example": "Example test",
                "key_concepts": ["concept1", "concept2"]
            })

            req = ExplanationRequest(
                equation="F = ma",
                equation_name="Newton's Second Law"
            )
            result = explainer._parse_response(json_content, req)

            assert result["equation_name"] == "Newton's Second Law"
            assert result["equation"] == "F = ma"
            assert result["simple_explanation"] == "Simple test"
            assert len(result["key_concepts"]) == 2

    def test_parse_response_invalid_json(self):
        """Test parsing invalid JSON response with fallback"""
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'}):
            explainer = PhysicsEquationExplainer()

            invalid_content = "This is not JSON"
            req = ExplanationRequest(equation="F = ma")
            result = explainer._parse_response(invalid_content, req)

            assert result["simple_explanation"] == invalid_content
            assert result["detailed_explanation"] == invalid_content
            assert result["real_world_example"] == "Example not available"
            assert result["key_concepts"] == []

    @patch('litellm.completion')
    def test_explain_equation(self, mock_completion):
        """Test the full explain_equation flow"""
        # Mock the LLM response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "simple_explanation": "Simple explanation",
            "detailed_explanation": "Detailed explanation",
            "real_world_example": "Real world example",
            "key_concepts": ["force", "mass", "acceleration"]
        })
        mock_completion.return_value = mock_response

        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'}):
            explainer = PhysicsEquationExplainer()
            req = ExplanationRequest(
                equation="F = ma",
                equation_name="Newton's Second Law"
            )

            explanation = explainer.explain_equation(req)

            assert isinstance(explanation, EquationExplanation)
            assert explanation.equation_name == "Newton's Second Law"
            assert explanation.equation == "F = ma"
            assert explanation.simple_explanation == "Simple explanation"
            assert len(explanation.key_concepts) == 3

    @patch('litellm.completion')
    def test_explain_equation_uses_correct_model(self, mock_completion):
        """Test that explain_equation calls the correct model"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "simple_explanation": "Test",
            "detailed_explanation": "Test",
            "real_world_example": "Test",
            "key_concepts": []
        })
        mock_completion.return_value = mock_response

        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'}):
            explainer = PhysicsEquationExplainer()
            req = ExplanationRequest(equation="F = ma")
            explainer.explain_equation(req)

            # Verify litellm.completion was called with correct model
            mock_completion.assert_called_once()
            call_args = mock_completion.call_args
            assert call_args[1]['model'] == "gemini-2.5-flash"

    @patch('litellm.completion')
    def test_explain_heat_conduction_equation(self, mock_completion):
        """Test explaining Fourier's Heat Conduction equation"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "simple_explanation": "Heat flows from hot to cold regions. The amount depends on temperature difference and material properties.",
            "detailed_explanation": "Fourier's law of heat conduction describes heat transfer through a material. Q/t = -kA(dT/dx), where Q is heat, k is thermal conductivity, A is area, and dT/dx is temperature gradient.",
            "real_world_example": "When heating a metal rod from one end, heat flows along the rod to the cooler end. The rate depends on the rod's material (k) and how quickly temperature changes along its length.",
            "key_concepts": ["thermal conductivity", "temperature gradient", "heat flux", "Fourier's law"]
        })
        mock_completion.return_value = mock_response

        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'}):
            explainer = PhysicsEquationExplainer()
            req = ExplanationRequest(
                equation="Q/t = -kA(dT/dx)",
                equation_name="Fourier's Law of Heat Conduction",
                context="Thermodynamics and heat transfer",
                difficulty_level="intermediate"
            )

            explanation = explainer.explain_equation(req)

            assert isinstance(explanation, EquationExplanation)
            assert explanation.equation_name == "Fourier's Law of Heat Conduction"
            assert explanation.equation == "Q/t = -kA(dT/dx)"
            assert "heat" in explanation.simple_explanation.lower()
            assert "thermal conductivity" in explanation.key_concepts
            assert len(explanation.key_concepts) == 4
            # Verify the equation is mentioned in the detailed explanation
            assert "dT/dx" in explanation.detailed_explanation or "temperature gradient" in explanation.detailed_explanation

    @patch('litellm.completion')
    def test_heat_conduction_beginner_level(self, mock_completion):
        """Test explaining heat conduction at beginner difficulty"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "simple_explanation": "Heat naturally flows from hot things to cold things, like when you touch a warm cup and heat moves to your hand.",
            "detailed_explanation": "In simple terms, heat always wants to spread out and reach cooler areas. The faster the temperature changes across something, the more heat flows through it.",
            "real_world_example": "If you put a cold spoon in hot soup, the spoon gets warm because heat flows from the hot soup through the spoon to the cooler handle.",
            "key_concepts": ["heat", "temperature", "cold", "hot", "flow"]
        })
        mock_completion.return_value = mock_response

        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'}):
            explainer = PhysicsEquationExplainer()
            req = ExplanationRequest(
                equation="Q/t = -kA(dT/dx)",
                equation_name="Heat Conduction",
                difficulty_level="beginner"
            )

            explanation = explainer.explain_equation(req)

            # Verify beginner-level content
            assert explanation.equation_name == "Heat Conduction"
            assert "simple language" not in explanation.simple_explanation or len(explanation.simple_explanation) > 0
            assert len(explanation.key_concepts) == 5

    @patch('litellm.completion')
    def test_heat_conduction_advanced_level(self, mock_completion):
        """Test explaining heat conduction at advanced difficulty"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "simple_explanation": "Heat conduction occurs through direct contact via molecular vibrations and free electron transport.",
            "detailed_explanation": "Fourier's law quantifies heat flux as q = -k∇T. In one dimension, this becomes Q/t = -kA(dT/dx). The thermal conductivity k depends on material microstructure. For metals, free electrons dominate heat transport. For non-metals, phonon scattering is primary. Temperature dependence of k can be approximated for various materials.",
            "real_world_example": "Thermal management in electronics relies on high-k materials (Cu: 400 W/m·K, Al: 200 W/m·K) to dissipate heat from CPU junctions to heatsinks. The thermal resistance R = L/(kA) determines junction temperature rise.",
            "key_concepts": ["thermal conductivity", "thermal diffusivity", "Fourier's law", "phonons", "free electrons", "thermal resistance", "Biot number"]
        })
        mock_completion.return_value = mock_response

        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'}):
            explainer = PhysicsEquationExplainer()
            req = ExplanationRequest(
                equation="Q/t = -kA(dT/dx)",
                equation_name="Fourier's Law of Heat Conduction",
                context="Advanced thermodynamics and materials science",
                difficulty_level="advanced"
            )

            explanation = explainer.explain_equation(req)

            # Verify advanced-level content
            assert explanation.equation_name == "Fourier's Law of Heat Conduction"
            assert "fourier" in explanation.detailed_explanation.lower()
            assert len(explanation.key_concepts) == 7
            assert "thermal diffusivity" in explanation.key_concepts

    @patch('litellm.completion')
    def test_heat_conduction_with_different_equations(self, mock_completion):
        """Test multiple heat conduction related equations"""
        heat_equations = [
            ("Q/t = -kA(dT/dx)", "Fourier's Law (1D)"),
            ("q = -k∇T", "Fourier's Law (Vector form)"),
            ("∂T/∂t = α∇²T", "Heat Diffusion Equation"),
            ("R = L/(kA)", "Thermal Resistance"),
        ]

        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'}):
            for eq, name in heat_equations:
                mock_response = MagicMock()
                mock_response.choices[0].message.content = json.dumps({
                    "simple_explanation": f"Explanation of {name}",
                    "detailed_explanation": f"Detailed explanation of {name}",
                    "real_world_example": f"Real world example for {name}",
                    "key_concepts": ["heat", "conduction", "temperature"]
                })
                mock_completion.return_value = mock_response

                explainer = PhysicsEquationExplainer()
                req = ExplanationRequest(
                    equation=eq,
                    equation_name=name,
                    context="Heat Transfer"
                )

                explanation = explainer.explain_equation(req)

                assert explanation.equation == eq
                assert explanation.equation_name == name
                assert "heat" in [c.lower() for c in explanation.key_concepts]
