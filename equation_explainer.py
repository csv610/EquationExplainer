import litellm
import json
from models import (
    EquationExplanation,
    EquationModel,
    HistoryModel,
    DerivationModel,
)


class PhysicsEquationExplainer:
    """LLM-powered physics equation explainer using litellm with Gemini"""

    def __init__(self, api_key: str = None):
        """
        Initialize the explainer with Gemini 2.5 Flash via OpenAI-compatible API.

        Args:
            api_key: Optional API key (if not provided, uses GOOGLE_API_KEY environment variable)
        """
        self.model = "gemini/gemini-2.5-flash"

    def _call_llm(self, prompt: str, system_prompt: str, response_model: type) -> object:
        """Make an LLM call with structured output"""
        response = litellm.completion(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            response_format=response_model,
        )
        return response.choices[0].message.parsed

    def _build_prompt(self, equation: EquationModel, response_model: type) -> str:
        """Build a prompt for the LLM based on the response model schema"""
        context_info = f"\nContext: {equation.context}" if equation.context else ""
        difficulty_info = f"\nDifficulty Level: {equation.difficulty}" if equation.difficulty else ""
        schema = response_model.model_json_schema()

        prompt = f"""Explain the following physics equation in detail:

Equation Name: {equation.name}
Equation: {equation.equation}{context_info}{difficulty_info}

Return the explanation in the following JSON format:
{json.dumps(schema, indent=2)}"""

        return prompt

    def explain_equation(self, equation: EquationModel) -> EquationExplanation:
        """
        Explain a physics equation using Gemini 2.5 Flash via litellm with structured output.

        Args:
            equation: EquationModel containing equation details

        Returns:
            EquationExplanation with detailed explanation
        """
        prompt = self._build_prompt(equation, EquationExplanation)
        explanation = self._call_llm(
            prompt=prompt,
            system_prompt="You are an expert physics teacher. Explain equations clearly and accurately.",
            response_model=EquationExplanation,
        )
        explanation.equation_name = equation.name
        explanation.equation = equation.equation
        return explanation

    def get_history(self, equation: EquationModel) -> HistoryModel:
        """
        Get historical context for a physics equation.

        Args:
            equation: EquationModel containing equation details

        Returns:
            HistoryModel with historical development information
        """
        prompt = self._build_prompt(equation, HistoryModel)
        history = self._call_llm(
            prompt=prompt,
            system_prompt="You are a physics historian. Provide accurate historical context for physics equations.",
            response_model=HistoryModel,
        )
        history.equation_name = equation.name
        history.equation = equation.equation
        return history

    def get_derivation(self, equation: EquationModel) -> DerivationModel:
        """
        Get mathematical derivation for a physics equation.

        Args:
            equation: EquationModel containing equation details

        Returns:
            DerivationModel with step-by-step derivation
        """
        prompt = self._build_prompt(equation, DerivationModel)
        derivation = self._call_llm(
            prompt=prompt,
            system_prompt="You are a physics professor. Derive equations step-by-step with clear mathematical reasoning.",
            response_model=DerivationModel,
        )
        derivation.equation_name = equation.name
        derivation.equation = equation.equation
        return derivation

    def get_available_equations(self) -> list[str]:
        """Return a list of available equations"""
        return [
            "Newton's Second Law",
            "Einstein's Mass-Energy Equivalence",
            "Schrödinger's Equation",
            "Wave Equation",
            "Heat Conduction Equation",
            "Maxwell's Equations",
            "Ohm's Law",
            "Ideal Gas Law",
            "Universal Law of Gravitation",
            "Coulomb's Law",
        ]

