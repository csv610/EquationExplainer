"""
Example usage of the Physics Equation Explainer app with Gemini 2.5 Flash.
"""

from equation_explainer import PhysicsEquationExplainer
from models import ExplanationRequest
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    # Initialize the explainer with Gemini 2.5 Flash via litellm
    # Make sure you have set GOOGLE_API_KEY in environment variables
    # Get your API key from: https://aistudio.google.com/app/apikey
    explainer = PhysicsEquationExplainer()

    # Example 1: Explain Newton's Second Law
    print("=" * 60)
    print("Example 1: Newton's Second Law")
    print("=" * 60)

    request1 = ExplanationRequest(
        equation="F = ma",
        equation_name="Newton's Second Law",
        context="Classical mechanics",
        difficulty_level="beginner",
    )

    explanation1 = explainer.explain_equation(request1)
    print(f"Equation: {explanation1.equation}")
    print(f"\nSimple Explanation:\n{explanation1.simple_explanation}")
    print(f"\nDetailed Explanation:\n{explanation1.detailed_explanation}")
    print(f"\nReal-World Example:\n{explanation1.real_world_example}")
    print(f"\nKey Concepts: {', '.join(explanation1.key_concepts)}")

    # Example 2: Explain Einstein's E=mc²
    print("\n" + "=" * 60)
    print("Example 2: Einstein's Mass-Energy Equivalence")
    print("=" * 60)

    request2 = ExplanationRequest(
        equation="E = mc²",
        equation_name="Einstein's Mass-Energy Equivalence",
        context="Modern physics and relativity",
        difficulty_level="intermediate",
    )

    explanation2 = explainer.explain_equation(request2)
    print(f"Equation: {explanation2.equation}")
    print(f"\nSimple Explanation:\n{explanation2.simple_explanation}")
    print(f"\nDetailed Explanation:\n{explanation2.detailed_explanation}")
    print(f"\nReal-World Example:\n{explanation2.real_world_example}")
    print(f"\nKey Concepts: {', '.join(explanation2.key_concepts)}")

    # Example 3: Multiple equations
    print("\n" + "=" * 60)
    print("Example 3: Multiple Equations")
    print("=" * 60)

    requests = [
        ExplanationRequest(equation="v = u + at", equation_name="Kinematic Equation", difficulty_level="beginner"),
        ExplanationRequest(equation="W = Fd cos(θ)", equation_name="Work", difficulty_level="intermediate"),
    ]

    explanations = explainer.explain_multiple(requests)
    for exp in explanations:
        print(f"\n{exp.equation_name}: {exp.equation}")
        print(f"Simple: {exp.simple_explanation[:100]}...")


if __name__ == "__main__":
    main()
