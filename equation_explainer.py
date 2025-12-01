import litellm
import json
import os
import re
from models import PhysicsEquation, EquationExplanation, EquationModel

class PhysicsEquationExplainer:
    """LLM-powered physics equation explainer using litellm with Gemini"""

    def __init__(self, api_key: str = None):
        """
        Initialize the explainer with Gemini 2.5 Flash via OpenAI-compatible API.

        Args:
            api_key: Optional API key (if not provided, uses GOOGLE_API_KEY environment variable)
        """
        self.model = "gemini/gemini-2.5-flash"

    #       litellm.api_key = os.environ.get("GEMINI_API_KEY")

    def explain_equation(self, equation: EquationModel) -> EquationExplanation:
        """
        Explain a physics equation using Gemini 2.5 Flash via litellm.

        Args:
            equation: EquationModel containing equation details

        Returns:
            EquationExplanation with detailed explanation
        """
        prompt = self._build_prompt(equation)

        response = litellm.completion(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert physics teacher. Explain equations clearly and accurately.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content
        explanation_data = self._parse_response(content, equation)

        return EquationExplanation(**explanation_data)

    def _build_prompt(self, equation: EquationModel) -> str:
        """Build a detailed prompt for the LLM"""
        context_info = f"\nContext: {equation.context}" if equation.context else ""

        # Get the schema from the EquationExplanation model
        schema = EquationExplanation.model_json_schema()

        prompt = f"""Explain the following physics equation in detail:

Equation Name: {equation.name}
Equation: {equation.equation}{context_info}

Please provide your response in the following JSON format:
{json.dumps(schema, indent=2)}

Return ONLY valid JSON, no additional text."""

        return prompt

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

    def _parse_response(self, content: str, equation: EquationModel) -> dict:
        """Parse the LLM response and validate against EquationExplanation model"""
        json_match = re.search(r"```json\n([\s\S]*?)\n```", content)
        json_str = json_match.group(1) if json_match else content

        try:
            explanation_data = json.loads(json_str)
        except json.JSONDecodeError:
            explanation_data = {
                "simple_explanation": content,
                "detailed_explanation": content,
                "real_world_example": "Example not available",
                "key_concepts": [],
            }

        return {
            "equation_name": equation.name,
            "equation": equation.equation,
            **explanation_data,
        }
