"""
Example usage of the Physics Equation Explainer.

Run:  python example.py
      python example.py -v    (verbose logging)
"""

import argparse
import logging

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from matheqs.equation_explainer import PhysicsEquationExplainer
from matheqs.models import EquationModel

console = Console()
logger = logging.getLogger(__name__)


def print_result(title: str, content: str) -> None:
    panel = Panel(
        Text(content, justify="left"),
        title=f"[bold cyan]{title}[/bold cyan]",
        border_style="cyan",
    )
    console.print(panel)


def main() -> None:
    parser = argparse.ArgumentParser(description="MathEqs usage example")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(message)s")

    console.print(Panel(
        Text("MathEqs Example Usage", justify="center", style="bold green"),
        border_style="blue",
    ))

    explainer = PhysicsEquationExplainer()

    # Example 1: Explain Newton's Second Law
    console.print("\n[bold]Example 1: Newton's Second Law[/bold]")

    equation = EquationModel(
        name="Newton's Second Law",
        equation="F = ma",
        context="Classical mechanics",
        difficulty="beginner",
    )

    explanation = explainer.explain_equation(equation)
    print_result("Equation", f"{equation.equation}")
    print_result("Simple Explanation", explanation.simple_explanation)
    print_result("Detailed Explanation", explanation.detailed_explanation)
    print_result("Real-World Example", explanation.real_world_example)
    print_result("Key Concepts", ", ".join(explanation.key_concepts))

    # Example 2: Get historical context for E=mc²
    console.print("\n[bold]Example 2: History of Einstein's Mass-Energy Equivalence[/bold]")

    equation = EquationModel(
        name="Einstein's Mass-Energy Equivalence",
        equation="E = mc²",
        context="Modern physics and relativity",
    )

    history = explainer.get_history(equation)
    print_result("Discoverer", f"{history.discoverer} ({history.year_discovered})")
    print_result("Historical Context", history.historical_context)
    print_result("Impact", history.impact)
    if history.source_citations:
        for cite in history.source_citations:
            print_result("Source", f"{cite.authors} ({cite.year}). {cite.title}. {cite.journal}.")

    # Example 3: Get derivation for a kinematic equation
    console.print("\n[bold]Example 3: Derivation of v = u + at[/bold]")

    equation = EquationModel(
        name="First Kinematic Equation",
        equation="v = u + at",
        context="Constant acceleration kinematics",
    )

    derivation = explainer.get_derivation(equation)
    print_result("Starting Principles", "\n".join(f"  • {p}" for p in derivation.starting_principles))
    for step in derivation.derivation_steps:
        details = f"  {step.description}"
        if step.mathematical_expression:
            details += f"\n  Expression: {step.mathematical_expression}"
        if step.reasoning:
            details += f"\n  Reasoning: {step.reasoning}"
        print_result(f"Step {step.step_number}: {step.title}", details)

    console.print("\n[bold green]✓ All examples completed successfully.[/bold green]")


if __name__ == "__main__":
    main()
