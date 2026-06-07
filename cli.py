"""
CLI application for Physics Equation Explainer and Analysis
"""

import argparse
import sys
from equation_explainer import PhysicsEquationExplainer

from models import (
    EquationModel,
)

from cli_utils import (
    print_header,
    print_section,
    print_subsection,
    print_list,
    generate_markdown_document,
    generate_four_section_markdown,
    save_markdown_file,
    print_error,
)


def build_equation(args, command: str) -> EquationModel:
    """Build an EquationModel from parsed CLI args"""
    eq_name = getattr(args, "name", None) or getattr(args, "equation_name", None) or args.equation
    return EquationModel(
        name=eq_name,
        equation=args.equation if hasattr(args, "equation") else eq_name,
        context=getattr(args, "context", None),
        difficulty=getattr(args, "difficulty", None),
    )


def explain_equation(args):
    """Handle explain subcommand"""
    try:
        print_header("Equation Explanation", subtitle="A detailed explanation of a physics equation.")

        explainer = PhysicsEquationExplainer()
        equation = build_equation(args, "explain")

        print("⏳ Analyzing equation...")
        explanation = explainer.explain_equation(equation)

        print_section("Equation", f"[bold]{explanation.equation_name}[/bold]\n{explanation.equation}")
        print_section("Simple Explanation", explanation.simple_explanation)
        print_section("Detailed Explanation", explanation.detailed_explanation)
        print_section("Real-World Example", explanation.real_world_example)
        print_section("Key Concepts", ", ".join(explanation.key_concepts))

        if hasattr(args, "md") and args.md:
            content_dict = {
                "Simple Explanation": explanation.simple_explanation,
                "Detailed Explanation": explanation.detailed_explanation,
                "Real-World Example": explanation.real_world_example,
                "Key Concepts": ", ".join(explanation.key_concepts),
            }
            markdown_content = generate_markdown_document(explanation.equation_name, explanation.equation, content_dict)
            filepath = save_markdown_file(markdown_content, args.md)
            print(f"✓ Markdown file saved to: {filepath}")

    except Exception as e:
        print_error(f"Failed to explain equation: {str(e)}")
        sys.exit(1)


def list_equations(args):
    """Handle list subcommand"""
    print_header("MathEqs - Physics Equation Explainer", subtitle="Your AI-powered physics equation assistant.")

    print(
        """
This tool can analyze ANY physics equation. Just enter the equation name or
expression, and get detailed explanations, historical context, and mathematical
derivations powered by AI.
"""
    )

    explainer = PhysicsEquationExplainer()
    equations = explainer.get_available_equations()
    print_list("Available Equations", equations)

    print("\nExamples")
    print("--------")
    print(
        """
  python cli.py "Newton's Second Law"
  python cli.py analyze "E = mc²" -m einstein.md
  python cli.py explain "F = ma"
  python cli.py history "Einstein's Mass-Energy"
  python cli.py derivation "Schrödinger's Equation"
  python cli.py explain "F = ma" -m equation.md
  python cli.py history "Wave Equation" -m wave_history.md
  python cli.py analyze "Heat Conduction" -d beginner -m heat.md
"""
    )


def history_equation(args):
    """Handle history subcommand"""
    try:
        print_header("Equation History", subtitle="The historical background of a physics equation.")
        print(f"⏳ Fetching history for: {args.equation_name}...")

        explainer = PhysicsEquationExplainer()
        equation = build_equation(args, "history")
        history = explainer.get_history(equation)

        print_section("Equation", f"[bold]{history.equation_name}[/bold]\n{history.equation}")
        print_section("Discovery", f"{history.discoverer} ({history.year_discovered})")

        if history.historical_context:
            print_section("Historical Context", history.historical_context)
        if history.earlier_related_equations:
            print_list("Earlier Related Equations", history.earlier_related_equations)
        if history.key_developments:
            print_list("Key Developments", history.key_developments)
        print_section("Impact", history.impact)
        if history.applications:
            for app in history.applications:
                print_subsection(app.title, app.description)

        if hasattr(args, "md") and args.md:
            content_parts = [
                f"**Discoverer:** {history.discoverer} ({history.year_discovered})",
                "",
                "**Historical Context**",
                history.historical_context,
            ]
            if history.key_developments:
                content_parts.extend(["", "**Key Developments**", *[f"- {d}" for d in history.key_developments]])
            content_parts.extend(["", "**Impact**", history.impact])

            content_dict = {"History": "\n".join(content_parts)}
            markdown_content = generate_markdown_document(f"History: {history.equation_name}", history.equation, content_dict)
            filepath = save_markdown_file(markdown_content, args.md)
            print(f"✓ Markdown file saved to: {filepath}")

    except Exception as e:
        print_error(f"Failed to get equation history: {str(e)}")
        sys.exit(1)


def derivation_equation(args):
    """Handle derivation subcommand"""
    try:
        print_header("Equation Derivation", subtitle="The mathematical derivation of a physics equation.")
        print(f"⏳ Fetching derivation for: {args.equation_name}...")

        explainer = PhysicsEquationExplainer()
        equation = build_equation(args, "derivation")
        derivation = explainer.get_derivation(equation)

        print_section("Equation", f"[bold]{derivation.equation_name}[/bold]\n{derivation.equation}")
        print_list("Starting Principles", derivation.starting_principles)

        for step in derivation.derivation_steps:
            header = f"Step {step.step_number}: {step.title}"
            details = step.description
            if step.mathematical_expression:
                details += f"\n\n{step.mathematical_expression}"
            if step.reasoning:
                details += f"\n\nReasoning: {step.reasoning}"
            print_section(header, details)

        if derivation.mathematical_prerequisites:
            print_list("Mathematical Prerequisites", derivation.mathematical_prerequisites)
        if derivation.validity_conditions:
            print_list("Validity Conditions", derivation.validity_conditions)
        if derivation.limitations:
            print_list("Limitations", derivation.limitations)
        if derivation.alternative_derivations:
            print_list("Alternative Derivations", derivation.alternative_derivations)

        if hasattr(args, "md") and args.md:
            steps_text = "\n\n".join(
                f"**Step {s.step_number}: {s.title}**\n{s.description}"
                + (f"\n\n{s.mathematical_expression}" if s.mathematical_expression else "")
                for s in derivation.derivation_steps
            )
            content_dict = {
                "Starting Principles": "\n".join(f"- {p}" for p in derivation.starting_principles),
                "Derivation Steps": steps_text,
            }
            if derivation.validity_conditions:
                content_dict["Validity Conditions"] = "\n".join(f"- {c}" for c in derivation.validity_conditions)
            if derivation.limitations:
                content_dict["Limitations"] = "\n".join(f"- {l}" for l in derivation.limitations)
            markdown_content = generate_markdown_document(
                f"Derivation: {derivation.equation_name}", derivation.equation, content_dict
            )
            filepath = save_markdown_file(markdown_content, args.md)
            print(f"✓ Markdown file saved to: {filepath}")

    except Exception as e:
        print_error(f"Failed to get equation derivation: {str(e)}")
        sys.exit(1)


def version(args):
    """Handle version subcommand"""
    print_header("MathEqs v1.0.0", subtitle="Physics Equation Explainer with AI.")
    print("\nAvailable Commands")
    print("-" * 18)
    print(
        """
  analyze     - Comprehensive analysis (4 sections: Intro, History, Derivation, Applications)
  explain     - Explain a physics equation
  history     - View equation history
  derivation  - View equation derivation
  list        - List available equations
  help        - Show help information
"""
    )


def comprehensive_equation_analysis(args):
    """Handle comprehensive analysis with all four sections"""
    try:
        print_header("Comprehensive Equation Analysis", subtitle="A complete analysis of a physics equation.")
        print(f"Equation: {args.equation_name}\n")

        explainer = PhysicsEquationExplainer()
        equation = build_equation(args, "analyze")

        introduction_content = ""
        history_content = ""
        derivation_content = ""
        applications_content = ""

        # 1. Introduction
        print("⏳ Generating introduction...")
        try:
            explanation = explainer.explain_equation(equation)
            introduction_content = (
                f"{explanation.simple_explanation}\n\n**Significance:** {explanation.detailed_explanation}"
            )
            print("✓ Introduction generated")
        except Exception as e:
            print(f"⚠️  Could not generate introduction: {str(e)}")

        # 2. History
        print("⏳ Generating history...")
        try:
            history = explainer.get_history(equation)
            history_content = (
                f"**Discoverer:** {history.discoverer} ({history.year_discovered})\n\n"
                f"**Historical Context:** {history.historical_context}\n\n"
                f"**Impact:** {history.impact}"
            )
            if history.key_developments:
                history_content += "\n\n**Key Developments:**\n" + "\n".join(f"- {d}" for d in history.key_developments)
            print("✓ History generated")
        except Exception as e:
            print(f"⚠️  Could not generate history: {str(e)}")

        # 3. Derivation
        print("⏳ Generating derivation...")
        try:
            derivation = explainer.get_derivation(equation)
            steps_text = "\n\n".join(
                f"**Step {s.step_number}: {s.title}**\n{s.description}"
                + (f"\n\n{s.mathematical_expression}" if s.mathematical_expression else "")
                for s in derivation.derivation_steps
            )
            derivation_content = (
                f"**Starting Principles:**\n" + "\n".join(f"- {p}" for p in derivation.starting_principles)
                + f"\n\n**Derivation Steps:**\n{steps_text}"
            )
            print("✓ Derivation generated")
        except Exception as e:
            print(f"⚠️  Could not generate derivation: {str(e)}")

        # 4. Applications
        print("⏳ Generating applications...")
        try:
            explanation = explainer.explain_equation(equation)
            applications_content = explanation.real_world_example
            print("✓ Applications generated")
        except Exception as e:
            print(f"⚠️  Could not generate applications: {str(e)}")

        if hasattr(args, "md") and args.md:
            markdown_content = generate_four_section_markdown(
                equation_name=args.equation_name,
                equation=args.equation_name,
                introduction=introduction_content,
                history=history_content,
                derivation=derivation_content,
                applications=applications_content,
            )
            filepath = save_markdown_file(markdown_content, args.md)
            print(f"\n✓ Complete analysis saved to: {filepath}")
        else:
            print_section("Introduction", introduction_content)
            print_section("History", history_content)
            print_section("Derivation", derivation_content)
            print_section("Applications", applications_content)

    except Exception as e:
        print_error(f"Failed to analyze equation: {str(e)}")
        sys.exit(1)


def handle_equation_input(equation_name: str):
    """Handle user input when equation name is provided - explains all aspects"""

    class Args:
        pass

    print_header("Physics Equation Analysis", subtitle="A complete analysis of a physics equation.")
    print(f"Equation: {equation_name}\n")

    args = Args()
    args.equation = equation_name
    args.name = None
    args.context = None
    args.difficulty = "intermediate"
    args.md = None

    print("[1/3] Explaining the equation...")
    explain_equation(args)

    print("\n[2/3] Fetching historical information...")
    args2 = Args()
    args2.equation_name = equation_name
    args2.context = None
    args2.difficulty = None
    args2.md = None
    history_equation(args2)

    print("\n[3/3] Fetching mathematical derivation...")
    args3 = Args()
    args3.equation_name = equation_name
    args3.context = None
    args3.difficulty = None
    args3.md = None
    derivation_equation(args3)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        prog="matheqs",
        description="MathEqs - Physics Equation Explainer",
        epilog="Examples:\n"
        "  python cli.py 'Wave Equation'\n"
        "  python cli.py analyze 'E = mc²' -m einstein.md\n"
        "  python cli.py explain 'F = ma'\n"
        '  python cli.py history "Newton\'s Second Law"\n'
        '  python cli.py derivation "Schrödinger\'s Equation"\n'
        "  python cli.py list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Explain command
    explain_parser = subparsers.add_parser("explain", help="Explain an equation")
    explain_parser.add_argument("equation", help="Physics equation to explain (e.g., 'F = ma')")
    explain_parser.add_argument("-n", "--name", help="Name of the equation")
    explain_parser.add_argument("-c", "--context", help="Additional context about the equation")
    explain_parser.add_argument(
        "-d",
        "--difficulty",
        choices=["beginner", "intermediate", "advanced"],
        default="intermediate",
        help="Difficulty level (default: intermediate)",
    )
    explain_parser.add_argument("-m", "--md", metavar="FILE", help="Save output to Markdown file")
    explain_parser.set_defaults(func=explain_equation)

    # History command
    history_parser = subparsers.add_parser("history", help="View equation history")
    history_parser.add_argument("equation_name", help="Name of the equation")
    history_parser.add_argument("-m", "--md", metavar="FILE", help="Save output to Markdown file")
    history_parser.set_defaults(func=history_equation)

    # Derivation command
    derivation_parser = subparsers.add_parser("derivation", help="View equation derivation")
    derivation_parser.add_argument("equation_name", help="Name of the equation")
    derivation_parser.add_argument("-m", "--md", metavar="FILE", help="Save output to Markdown file")
    derivation_parser.set_defaults(func=derivation_equation)

    # Analyze command (comprehensive 4-section analysis)
    analyze_parser = subparsers.add_parser(
        "analyze", help="Comprehensive analysis with 4 sections: Introduction, History, Derivation, Applications"
    )
    analyze_parser.add_argument("equation_name", help="Name of the equation")
    analyze_parser.add_argument(
        "-d",
        "--difficulty",
        choices=["beginner", "intermediate", "advanced"],
        default="intermediate",
        help="Difficulty level (default: intermediate)",
    )
    analyze_parser.add_argument("-m", "--md", metavar="FILE", help="Save output to Markdown file")
    analyze_parser.set_defaults(func=comprehensive_equation_analysis)

    # List command
    list_parser = subparsers.add_parser("list", help="List available equations")
    list_parser.set_defaults(func=list_equations)

    # Version command
    version_parser = subparsers.add_parser("version", help="Show version")
    version_parser.set_defaults(func=version)

    return parser


def main():
    """Main CLI entry point"""
    known_commands = ["explain", "history", "derivation", "analyze", "list", "version"]

    if len(sys.argv) > 1 and sys.argv[1] not in known_commands and not sys.argv[1].startswith("-"):
        equation_name = sys.argv[1]
        handle_equation_input(equation_name)
        return

    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
