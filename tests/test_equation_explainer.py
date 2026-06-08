"""Tests for PhysicsEquationExplainer"""
from unittest.mock import MagicMock, patch

import pytest

from matheqs.equation_explainer import PhysicsEquationExplainer
from matheqs.models import EquationExplanation, EquationModel


class TestPhysicsEquationExplainer:

    def test_init_defaults(self):
        explainer = PhysicsEquationExplainer()
        assert explainer.model == "ollama/gemma4"
        assert explainer.temperature == 0.7
        assert explainer.seed is None
        assert explainer.max_retries == 3

    def test_init_custom_model(self):
        explainer = PhysicsEquationExplainer(model="gpt-4o", temperature=0.2)
        assert explainer.model == "gpt-4o"
        assert explainer.temperature == 0.2

    def test_init_with_seed(self):
        explainer = PhysicsEquationExplainer(model="gpt-4o", seed=42)
        assert explainer.seed == 42

    def test_repr_no_seed(self):
        explainer = PhysicsEquationExplainer(model="gpt-4o", temperature=0.5)
        assert repr(explainer) == "PhysicsEquationExplainer(model='gpt-4o', temperature=0.5)"

    def test_repr_with_seed(self):
        explainer = PhysicsEquationExplainer(model="gpt-4o", seed=42)
        assert "seed=42" in repr(explainer)

    def test_build_prompt_basic(self):
        explainer = PhysicsEquationExplainer()
        equation = EquationModel(name="Newton's Second Law", equation="F = ma")
        prompt = explainer._build_prompt(equation, "explain")
        assert "F = ma" in prompt
        assert "Newton's Second Law" in prompt
        assert "Target audience" not in prompt

    def test_build_prompt_with_context(self):
        explainer = PhysicsEquationExplainer()
        equation = EquationModel(
            name="Newton's Second Law", equation="F = ma", context="Classical mechanics"
        )
        prompt = explainer._build_prompt(equation, "explain")
        assert "Classical mechanics" in prompt

    def test_build_prompt_with_difficulty(self):
        explainer = PhysicsEquationExplainer()
        equation = EquationModel(
            name="Newton's Second Law", equation="F = ma", difficulty="beginner"
        )
        prompt = explainer._build_prompt(equation, "explain")
        assert "Target audience:** beginner" in prompt

    def test_build_prompt_task_label(self):
        explainer = PhysicsEquationExplainer()
        equation = EquationModel(name="Test", equation="F = ma")
        prompt = explainer._build_prompt(equation, "history")
        assert "History of" in prompt

    @patch('litellm.completion')
    def test_explain_equation(self, mock_completion):
        mock_response = MagicMock()
        mock_explanation = EquationExplanation(
            simple_explanation="Simple explanation",
            detailed_explanation="Detailed explanation",
            real_world_example="Real world example",
            key_concepts=["force", "mass", "acceleration"],
        )
        mock_response.choices[0].message.parsed = mock_explanation
        mock_completion.return_value = mock_response

        explainer = PhysicsEquationExplainer()
        equation = EquationModel(name="Newton's Second Law", equation="F = ma")
        explanation = explainer.explain_equation(equation)

        assert isinstance(explanation, EquationExplanation)
        assert explanation.simple_explanation == "Simple explanation"
        assert len(explanation.key_concepts) == 3

    @patch('litellm.completion')
    def test_explain_equation_uses_correct_model(self, mock_completion):
        mock_response = MagicMock()
        mock_response.choices[0].message.parsed = EquationExplanation(
            simple_explanation="", detailed_explanation="",
            real_world_example="", key_concepts=[],
        )
        mock_completion.return_value = mock_response

        explainer = PhysicsEquationExplainer(model="my-custom-model", temperature=0.1)
        equation = EquationModel(name="Test", equation="E = mc²")
        explainer.explain_equation(equation)

        mock_completion.assert_called_once()
        kwargs = mock_completion.call_args[1]
        assert kwargs["model"] == "my-custom-model"
        assert kwargs["temperature"] == 0.1

    @patch('litellm.completion')
    def test_explain_equation_passes_seed(self, mock_completion):
        mock_response = MagicMock()
        mock_response.choices[0].message.parsed = EquationExplanation(
            simple_explanation="", detailed_explanation="",
            real_world_example="", key_concepts=[],
        )
        mock_completion.return_value = mock_response

        explainer = PhysicsEquationExplainer(model="gpt-4o", seed=42)
        equation = EquationModel(name="Test", equation="F = ma")
        explainer.explain_equation(equation)

        assert mock_completion.call_args[1].get("seed") == 42

    @patch('litellm.completion')
    def test_explain_equation_uses_response_format(self, mock_completion):
        mock_response = MagicMock()
        mock_response.choices[0].message.parsed = EquationExplanation(
            simple_explanation="", detailed_explanation="",
            real_world_example="", key_concepts=[],
        )
        mock_completion.return_value = mock_response

        explainer = PhysicsEquationExplainer()
        equation = EquationModel(name="Test", equation="F = ma")
        explainer.explain_equation(equation)

        assert mock_completion.call_args[1]["response_format"] == EquationExplanation

    @patch('litellm.completion')
    def test_get_history(self, mock_completion):
        from matheqs.models import HistoryModel
        mock_response = MagicMock()
        mock_history = HistoryModel(
            year_discovered=1687,
            discoverer="Isaac Newton",
            historical_context="Developed during the Scientific Revolution",
            impact="Foundation of classical mechanics",
        )
        mock_response.choices[0].message.parsed = mock_history
        mock_completion.return_value = mock_response

        explainer = PhysicsEquationExplainer()
        equation = EquationModel(name="Newton's Second Law", equation="F = ma")
        history = explainer.get_history(equation)

        assert isinstance(history, HistoryModel)
        assert history.discoverer == "Isaac Newton"
        assert history.year_discovered == 1687

    @patch('litellm.completion')
    def test_get_derivation(self, mock_completion):
        from matheqs.models import DerivationModel, DerivationStep
        mock_response = MagicMock()
        mock_derivation = DerivationModel(
            starting_principles=["Work-energy theorem"],
            derivation_steps=[
                DerivationStep(
                    step_number=1, title="Start with work",
                    description="Work equals force times distance",
                    mathematical_expression="W = Fd",
                    reasoning="Definition of work",
                )
            ],
        )
        mock_response.choices[0].message.parsed = mock_derivation
        mock_completion.return_value = mock_response

        explainer = PhysicsEquationExplainer()
        equation = EquationModel(name="Kinetic Energy", equation="KE = (1/2)mv²")
        derivation = explainer.get_derivation(equation)

        assert isinstance(derivation, DerivationModel)
        assert len(derivation.derivation_steps) == 1
        assert derivation.derivation_steps[0].title == "Start with work"

    @patch('litellm.completion')
    def test_call_llm_raises_on_empty_choices(self, mock_completion):
        mock_response = MagicMock()
        mock_response.choices = []
        mock_completion.return_value = mock_response

        explainer = PhysicsEquationExplainer()
        equation = EquationModel(name="Test", equation="x = y")
        with pytest.raises(RuntimeError, match="no choices"):
            explainer.explain_equation(equation)

    @patch('litellm.completion')
    def test_call_llm_raises_on_none_parsed(self, mock_completion):
        mock_response = MagicMock()
        mock_response.choices[0].message.parsed = None
        mock_completion.return_value = mock_response

        explainer = PhysicsEquationExplainer()
        equation = EquationModel(name="Test", equation="x = y")
        with pytest.raises(RuntimeError, match="no parsed response"):
            explainer.explain_equation(equation)

    def test_retry_on_generic_error(self):
        call_count = 0

        def _fail_twice(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RuntimeError("API error")
            mock = MagicMock()
            mock.choices[0].message.parsed = EquationExplanation(
                simple_explanation="", detailed_explanation="",
                real_world_example="", key_concepts=[],
            )
            return mock

        with patch('litellm.completion', side_effect=_fail_twice):
            explainer = PhysicsEquationExplainer(max_retries=3)
            equation = EquationModel(name="Test", equation="x = y")
            explainer.explain_equation(equation)
            assert call_count == 3

    def test_retry_exhausted(self):
        call_count = 0

        def _always_fail(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise RuntimeError("Persistent error")

        with patch('litellm.completion', side_effect=_always_fail):
            explainer = PhysicsEquationExplainer(max_retries=2)
            equation = EquationModel(name="Test", equation="x = y")
            with pytest.raises(RuntimeError, match="failed after 2 attempts"):
                explainer.explain_equation(equation)
            assert call_count == 2

    def test_auth_error_no_retry(self):
        call_count = 0

        class FakeAuthError(Exception):
            pass

        def _fail_once(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise FakeAuthError("Bad key")

        with (
            patch('matheqs.equation_explainer.litellm.AuthenticationError', FakeAuthError),
            patch('matheqs.equation_explainer.litellm.completion', side_effect=_fail_once),
        ):
                explainer = PhysicsEquationExplainer(max_retries=3)
                equation = EquationModel(name="Test", equation="x = y")
                with pytest.raises(RuntimeError, match="Authentication failed"):
                    explainer.explain_equation(equation)
                assert call_count == 1

    def test_get_available_equations(self):
        equations = PhysicsEquationExplainer.get_available_equations()
        assert isinstance(equations, list)
        assert len(equations) > 0
        assert "Newton's Second Law" in equations

    def test_available_equations_contains_known(self):
        assert "Newton's Second Law" in PhysicsEquationExplainer.get_available_equations()
        assert "Einstein's Mass-Energy Equivalence" in PhysicsEquationExplainer.get_available_equations()

    def test_pseudoscience_keywords(self):
        keywords = PhysicsEquationExplainer.get_pseudoscience_keywords()
        assert isinstance(keywords, list)
        assert "perpetual motion" in keywords

    def test_rate_limit_retry_exhausted(self):
        call_count = 0

        class FakeRateLimitError(Exception):
            pass

        def _fail(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise FakeRateLimitError("rate limit")

        with (
            patch('matheqs.equation_explainer.litellm.RateLimitError', FakeRateLimitError),
            patch('matheqs.equation_explainer.litellm.completion', side_effect=_fail),
        ):
                explainer = PhysicsEquationExplainer(max_retries=2)
                equation = EquationModel(name="Test", equation="x = y")
                with pytest.raises(RuntimeError, match="failed after 2 attempts"):
                    explainer.explain_equation(equation)
                assert call_count == 2

    def test_api_connection_error_retry(self):
        call_count = 0

        class FakeAPIError(Exception):
            pass

        def _fail(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise FakeAPIError("connection error")

        with (
            patch('matheqs.equation_explainer.litellm.APIConnectionError', FakeAPIError),
            patch('matheqs.equation_explainer.litellm.ServiceUnavailableError', FakeAPIError),
            patch('matheqs.equation_explainer.litellm.completion', side_effect=_fail),
        ):
                    explainer = PhysicsEquationExplainer(max_retries=2)
                    equation = EquationModel(name="Test", equation="x = y")
                    with pytest.raises(RuntimeError, match="failed after 2 attempts"):
                        explainer.explain_equation(equation)
                    assert call_count == 2

    def test_timeout_retry(self):
        call_count = 0

        class FakeTimeoutError(Exception):
            pass

        def _fail(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise FakeTimeoutError("timeout")

        with (
            patch('matheqs.equation_explainer.litellm.Timeout', FakeTimeoutError),
            patch('matheqs.equation_explainer.litellm.completion', side_effect=_fail),
        ):
                explainer = PhysicsEquationExplainer(max_retries=2)
                equation = EquationModel(name="Test", equation="x = y")
                with pytest.raises(RuntimeError, match="failed after 2 attempts"):
                    explainer.explain_equation(equation)
                assert call_count == 2

    def test_pseudoscience_detection_logs_warning(self, caplog):
        caplog.set_level("WARNING")
        mock_response = MagicMock()
        mock_response.choices[0].message.parsed = EquationExplanation(
            simple_explanation="", detailed_explanation="",
            real_world_example="", key_concepts=[],
        )
        explainer = PhysicsEquationExplainer()
        equation = EquationModel(
            name="Free Energy Machine", equation="E = mc²"
        )
        with patch('litellm.completion', return_value=mock_response):
            explainer._call_with_overrides(equation, EquationExplanation, "explain")
        assert any("pseudoscience" in msg.lower() for msg in caplog.messages)
