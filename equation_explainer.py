import litellm
from models import EquationExplanation, EquationModel

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
        Explain a physics equation using Gemini 2.5 Flash via litellm with structured output.

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
            response_format=EquationExplanation,
        )

        # Extract parsed response - litellm returns the Pydantic model
        explanation = response.choices[0].message.parsed

        # Update equation details from input
        explanation.equation_name = equation.name
        explanation.equation = equation.equation

        return explanation

    def _build_prompt(self, equation: EquationModel) -> str:
        """Build a detailed prompt for the LLM"""
        context_info = f"\nContext: {equation.context}" if equation.context else ""

        prompt = f"""Explain the following physics equation in detail:

Equation Name: {equation.name}
Equation: {equation.equation}{context_info}

Provide a comprehensive explanation with:
- simple_explanation: A beginner-friendly explanation
- detailed_explanation: A more technical explanation with deeper insights
- real_world_example: Practical applications of this equation
- key_concepts: Important concepts related to this equation"""

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

