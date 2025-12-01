"""
CLI application for Physics Equation Explainer and Analysis
Uses only standard library (argparse)
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
    generate_markdown_document,
    generate_four_section_markdown,
    save_markdown_file,
    print_error,
    print_list,
)


def explain_equation(args):
    """Handle explain subcommand"""
    try:
        print_header("Equation Explanation", subtitle="A detailed explanation of a physics equation.")

        # Initialize explainer
        explainer = PhysicsEquationExplainer()

        # Create equation model
        equation = EquationModel(
            name=args.name or args.equation,
            equation=args.equation,
            context=args.context,
        )

        # Explain equation
        print("⏳ Analyzing equation...")
        explanation = explainer.explain_equation(equation)

        # Display equation info
        print_section("Equation", f"[bold]{explanation.equation_name}[/bold]\n{explanation.equation}")

        # Display sections
        print_section("Simple Explanation", explanation.simple_explanation)
        print_section("Detailed Explanation", explanation.detailed_explanation)
        print_section("Real-World Example", explanation.real_world_example)

        # Key Concepts
        concepts = ", ".join(explanation.key_concepts)
        print_section("Key Concepts", concepts)

        # Generate Markdown file if requested
        if hasattr(args, "md") and args.md:
            content_dict = {
                "Simple Explanation": explanation.simple_explanation,
                "Detailed Explanation": explanation.detailed_explanation,
                "Real-World Example": explanation.real_world_example,
                "Key Concepts": concepts,
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
  python cli.py explain "F = ma" --md equation.md
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

        # Create equation model to get history info
        equation = EquationModel(
            name=args.equation_name,
            equation=args.equation_name,
            context="Provide historical information about this equation including discoverer, year discovered, historical context, and modern applications.",
        )

        explanation = explainer.explain_equation(equation)

        print_section("Equation", f"[bold]{explanation.equation_name}[/bold]\n{explanation.equation}")

        print_section("Description", explanation.simple_explanation)
        print_section("Detailed Information", explanation.detailed_explanation)
        print_section("Modern Applications", explanation.real_world_example)

        concepts = ", ".join(explanation.key_concepts)
        print_section("Key Concepts", concepts)

        # Generate Markdown file if requested
        if hasattr(args, "md") and args.md:
            content_dict = {
                "Description": explanation.simple_explanation,
                "Detailed Information": explanation.detailed_explanation,
                "Modern Applications": explanation.real_world_example,
                "Key Concepts": concepts,
            }
            markdown_content = generate_markdown_document(
                f"History: {explanation.equation_name}", explanation.equation, content_dict
            )
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

        # Create equation model to get derivation info
        equation = EquationModel(
            name=args.equation_name,
            equation=args.equation_name,
            context="Provide a detailed mathematical derivation of this equation, including the starting principles, key assumptions, step-by-step derivation steps, and limitations.",
        )

        explanation = explainer.explain_equation(equation)

        print_section("Equation", f"[bold]{explanation.equation_name}[/bold]\n{explanation.equation}")

        print_section("Starting Principles & Foundations", explanation.simple_explanation)
        print_section("Derivation Details", explanation.detailed_explanation)
        print_section("Assumptions & Limitations", explanation.real_world_example)

        concepts = ", ".join(explanation.key_concepts)
        print_section("Key Concepts", concepts)

        # Generate Markdown file if requested
        if hasattr(args, "md") and args.md:
            content_dict = {
                "Starting Principles & Foundations": explanation.simple_explanation,
                "Derivation Details": explanation.detailed_explanation,
                "Assumptions & Limitations": explanation.real_world_example,
                "Key Concepts": concepts,
            }
            markdown_content = generate_markdown_document(
                f"Derivation: {explanation.equation_name}", explanation.equation, content_dict
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

        # Collect all sections
        introduction_content = ""
        history_content = ""
        derivation_content = ""
        applications_content = ""

        # 1. Introduction
        print("⏳ Generating introduction...")
        try:
            equation = EquationModel(
                name=args.equation_name,
                equation=args.equation_name,
                context="Provide a comprehensive introduction to this equation, including its overview, significance, and the field of physics it belongs to.",
            )
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
            equation = EquationModel(
                name=args.equation_name,
                equation=args.equation_name,
                context="Provide the historical development of this equation, including when it was discovered, who discovered it, and how it evolved.",
            )
            explanation = explainer.explain_equation(equation)
            history_content = f"{explanation.simple_explanation}\n\n{explanation.detailed_explanation}"
            print("✓ History generated")
        except Exception as e:
            print(f"⚠️  Could not generate history: {str(e)}")

        # 3. Derivation
        print("⏳ Generating derivation...")
        try:
            equation = EquationModel(
                name=args.equation_name,
                equation=args.equation_name,
                context="Provide a detailed mathematical derivation of this equation, including the starting principles, key assumptions, step-by-step derivation, and limitations.",
            )
            explanation = explainer.explain_equation(equation)
            derivation_content = f"{explanation.simple_explanation}\n\n{explanation.detailed_explanation}"
            print("✓ Derivation generated")
        except Exception as e:
            print(f"⚠️  Could not generate derivation: {str(e)}")

        # 4. Applications
        print("⏳ Generating applications...")
        try:
            equation = EquationModel(
                name=args.equation_name,
                equation=args.equation_name,
                context="Provide modern applications and practical uses of this equation in technology, engineering, and science.",
            )
            explanation = explainer.explain_equation(equation)
            applications_content = f"{explanation.simple_explanation}\n\n{explanation.detailed_explanation}"
            print("✓ Applications generated")
        except Exception as e:
            print(f"⚠️  Could not generate applications: {str(e)}")

        # Generate markdown with all four sections
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
            # Print to console
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

    # Explain the equation
    print("[1/3] Explaining the equation...")
    args = Args()
    args.equation = equation_name
    args.name = None
    args.context = None
    args.difficulty = "intermediate"
    args.md = None
    explain_equation(args)

    # Get history
    print("\n[2/3] Fetching historical information...")
    args = Args()
    args.equation_name = equation_name
    args.json = False
    args.md = None
    history_equation(args)

    # Get derivation
    print("\n[3/3] Fetching mathematical derivation...")
    args = Args()
    args.equation_name = equation_name
    args.step = None
    args.json = False
    args.md = None
    derivation_equation(args)


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
    history_parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    history_parser.add_argument("-m", "--md", metavar="FILE", help="Save output to Markdown file")
    history_parser.set_defaults(func=history_equation)

    # Derivation command
    derivation_parser = subparsers.add_parser("derivation", help="View equation derivation")
    derivation_parser.add_argument("equation_name", help="Name of the equation")
    derivation_parser.add_argument("-s", "--step", type=int, help="Show specific derivation step")
    derivation_parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
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
    # Check if first argument is a known command before parsing
    known_commands = ["explain", "history", "derivation", "analyze", "list", "version"]

    if len(sys.argv) > 1 and sys.argv[1] not in known_commands and not sys.argv[1].startswith("-"):
        # Treat as equation name and prompt user for action
        equation_name = sys.argv[1]
        handle_equation_input(equation_name)
        return

    parser = create_parser()
    args = parser.parse_args()

    # Show help if no command given
    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Execute command
    args.func(args)


if __name__ == "__main__":
    main()
