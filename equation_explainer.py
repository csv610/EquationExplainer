import litellm
import json
import os
import re
from models import PhysicsEquation, EquationExplanation, ExplanationRequest

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

    def explain_equation(self, request: ExplanationRequest) -> EquationExplanation:
        """
        Explain a physics equation using Gemini 2.5 Flash via litellm.

        Args:
            request: ExplanationRequest containing equation and context

        Returns:
            EquationExplanation with detailed explanation
        """
        prompt = self._build_prompt(request)

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
        explanation_data = self._parse_response(content, request)

        return EquationExplanation(**explanation_data)

    def _build_prompt(self, request: ExplanationRequest) -> str:
        """Build a detailed prompt for the LLM"""
        difficulty_guidance = {
            "beginner": "Use simple language and avoid advanced terminology. Focus on intuition.",
            "intermediate": "Balance simplicity with technical accuracy. Include mathematical details.",
            "advanced": "Use precise technical language and advanced concepts. Dive deep into applications.",
        }

        guidance = difficulty_guidance.get(request.difficulty_level, difficulty_guidance["intermediate"])

        context_info = f"\nContext: {request.context}" if request.context else ""
        equation_name_info = f"\nEquation Name: {request.equation_name}" if request.equation_name else ""

        # Get the schema from the EquationExplanation model
        schema = EquationExplanation.model_json_schema()

        prompt = f"""Explain the following physics equation in detail:

Equation: {request.equation}{equation_name_info}{context_info}

Please provide your response in the following JSON format:
{json.dumps(schema, indent=2)}

Difficulty Level: {request.difficulty_level}
Guidance: {guidance}

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

    def _parse_response(self, content: str, request: ExplanationRequest) -> dict:
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
            "equation_name": request.equation_name or "Physics Equation",
            "equation": request.equation,
            **explanation_data,
        }
