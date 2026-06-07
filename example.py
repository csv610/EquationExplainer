"""
Example usage of the Physics Equation Explainer app with Gemini 2.5 Flash.
"""

from equation_explainer import PhysicsEquationExplainer
from models import EquationModel


def main():
    explainer = PhysicsEquationExplainer()

    # Example 1: Explain Newton's Second Law
    print("=" * 60)
    print("Example 1: Newton's Second Law")
    print("=" * 60)

    equation = EquationModel(
        name="Newton's Second Law",
        equation="F = ma",
        context="Classical mechanics",
        difficulty="beginner",
    )

    explanation = explainer.explain_equation(equation)
    print(f"Equation: {explanation.equation}")
    print(f"\nSimple Explanation:\n{explanation.simple_explanation}")
    print(f"\nDetailed Explanation:\n{explanation.detailed_explanation}")
    print(f"\nReal-World Example:\n{explanation.real_world_example}")
    print(f"\nKey Concepts: {', '.join(explanation.key_concepts)}")

    # Example 2: Get historical context for E=mc²
    print("\n" + "=" * 60)
    print("Example 2: History of Einstein's Mass-Energy Equivalence")
    print("=" * 60)

    equation = EquationModel(
        name="Einstein's Mass-Energy Equivalence",
        equation="E = mc²",
        context="Modern physics and relativity",
    )

    history = explainer.get_history(equation)
    print(f"Equation: {history.equation}")
    print(f"\nDiscoverer: {history.discoverer} ({history.year_discovered})")
    print(f"\nHistorical Context:\n{history.historical_context}")
    print(f"\nImpact:\n{history.impact}")

    # Example 3: Get derivation for a kinematic equation
    print("\n" + "=" * 60)
    print("Example 3: Derivation of v = u + at")
    print("=" * 60)

    equation = EquationModel(
        name="First Kinematic Equation",
        equation="v = u + at",
        context="Constant acceleration kinematics",
    )

    derivation = explainer.get_derivation(equation)
    print(f"Equation: {derivation.equation}")
    print(f"\nStarting Principles:")
    for p in derivation.starting_principles:
        print(f"  • {p}")
    print(f"\nDerivation Steps:")
    for step in derivation.derivation_steps:
        print(f"\n  Step {step.step_number}: {step.title}")
        print(f"  {step.description}")
        if step.mathematical_expression:
            print(f"  Expression: {step.mathematical_expression}")


if __name__ == "__main__":
    main()
