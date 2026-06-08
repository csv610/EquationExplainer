"""
CLI application for Physics Equation Explainer and Analysis
"""

import argparse
import logging
import os
import sys

from dotenv import load_dotenv

from matheqs.cli_utils import (
    generate_four_section_markdown,
    generate_markdown_document,
    print_error,
    print_header,
    print_list,
    print_section,
    print_subsection,
    print_text,
    save_markdown_file,
)
from matheqs.equation_explainer import PhysicsEquationExplainer
from matheqs.models import (
    EquationModel,
)

logger = logging.getLogger(__name__)

VERSION = "1.0.0"

load_dotenv()

_KNOWN_API_KEYS = {
    "OPENAI_API_KEY": "OpenAI",
    "GEMINI_API_KEY": "Google Gemini",
    "ANTHROPIC_API_KEY": "Anthropic",
    "GOOGLE_API_KEY": "Google AI",
    "AZURE_API_KEY": "Azure OpenAI",
    "MISTRAL_API_KEY": "Mistral",
    "DEEPSEEK_API_KEY": "DeepSeek",
    "COHERE_API_KEY": "Cohere",
    "TOGETHER_API_KEY": "Together",
    "GROQ_API_KEY": "Groq",
}


def _check_api_key(model: str | None) -> None:
    if model and model.startswith("ollama/"):
        return
    found = [name for var, name in _KNOWN_API_KEYS.items() if os.environ.get(var)]
    if not found:
        print_text(
            "Warning: No API keys found in environment. "
            "Set one of: " + ", ".join(_KNOWN_API_KEYS) + ". "
            "Or use a local Ollama model with -m ollama/<model>.",
            style="yellow",
        )


def _make_explainer(args: argparse.Namespace) -> PhysicsEquationExplainer:
    kwargs = {}
    model = getattr(args, "model", None)
    if model:
        kwargs["model"] = model
    seed = getattr(args, "seed", None)
    if seed is not None:
        kwargs["seed"] = seed
    return PhysicsEquationExplainer(**kwargs)


def _build_equation(args: argparse.Namespace) -> EquationModel:
    eq_name = getattr(args, "name", None) or getattr(args, "equation_name", None) or args.equation
    return EquationModel(
        name=eq_name,
        equation=args.equation if hasattr(args, "equation") else eq_name,
        context=getattr(args, "context", None),
        difficulty=getattr(args, "difficulty", None),
    )


def _save_if_requested(args: argparse.Namespace, title: str, equation: str, content_dict: dict[str, str]) -> None:
    if hasattr(args, "output") and args.output:
        markdown_content = generate_markdown_document(title, equation, content_dict)
        filepath = save_markdown_file(markdown_content, args.output)
        print_text(f"✓ Markdown file saved to: {filepath}", style="green")


def _format_year(year: int | None) -> str:
    return str(year) if year is not None else "Unknown"


def explain_equation(args: argparse.Namespace) -> None:
    if not getattr(args, "_quiet", False):
        print_header("Equation Explanation", subtitle="A detailed explanation of a physics equation.")
    explainer = _make_explainer(args)
    equation = _build_equation(args)
    logger.info("Explaining equation: %s", equation.name)
    explanation = explainer.explain_equation(equation)

    print_section("Equation", f"[bold]{equation.name}[/bold]\n{equation.equation}")
    print_section("Simple Explanation", explanation.simple_explanation)
    print_section("Detailed Explanation", explanation.detailed_explanation)
    print_section("Real-World Example", explanation.real_world_example)
    print_section("Key Concepts", ", ".join(explanation.key_concepts))

    _save_if_requested(args, equation.name, equation.equation, {
        "Simple Explanation": explanation.simple_explanation,
        "Detailed Explanation": explanation.detailed_explanation,
        "Real-World Example": explanation.real_world_example,
        "Key Concepts": ", ".join(explanation.key_concepts),
    })


def list_equations(args: argparse.Namespace) -> None:
    print_header("MathEqs - Physics Equation Explainer", subtitle="Your AI-powered physics equation assistant.")
    print_text(
        "This tool can analyze ANY physics equation. Just enter the equation name or "
        "expression, and get detailed explanations, historical context, and mathematical "
        "derivations powered by AI.",
        style="cyan",
    )
    equations = PhysicsEquationExplainer.get_available_equations()
    print_list("Sample Equations", equations)

    print_text("\n[bold]Examples[/bold]", style="")
    print_text(
        '  python cli.py "Newton\'s Second Law"\n'
        '  python cli.py analyze "E = mc²" -o einstein.md\n'
        '  python cli.py -m gpt-4o explain "F = ma"\n'
        '  python cli.py history "Newton\'s Second Law"\n'
        '  python cli.py derivation "Schrödinger\'s Equation"\n'
        '  python cli.py explain "F = ma" -o equation.md\n'
        '  python cli.py history "Wave Equation" -o wave_history.md\n'
        '  python cli.py analyze "Heat Conduction" -d beginner -o heat.md',
        style="cyan",
    )


def history_equation(args: argparse.Namespace) -> None:
    if not getattr(args, "_quiet", False):
        print_header("Equation History", subtitle="The historical background of a physics equation.")
    logger.info("Fetching history for: %s", args.equation_name)
    explainer = _make_explainer(args)
    equation = _build_equation(args)
    history = explainer.get_history(equation)

    print_section("Equation", f"[bold]{equation.name}[/bold]\n{equation.equation}")
    print_section("Discovery", f"{history.discoverer} ({_format_year(history.year_discovered)})")

    if history.historical_context:
        print_section("Historical Context", history.historical_context)
    if history.earlier_related_equations:
        print_list("Earlier Related Equations", history.earlier_related_equations)
    if history.key_developments:
        print_list("Key Developments", history.key_developments)
    print_section("Impact", history.impact)
    if history.source_citations:
        print_list("Sources", [f"{c.authors} ({c.year}). {c.title}. {c.journal}." for c in history.source_citations])
    if history.applications:
        for app in history.applications:
            print_subsection(app.title, app.description)

    if hasattr(args, "output") and args.output:
        year_str = _format_year(history.year_discovered)
        content_parts = [
            f"**Discoverer:** {history.discoverer} ({year_str})",
            "",
            "**Historical Context**",
            history.historical_context,
        ]
        if history.key_developments:
            content_parts.extend(["", "**Key Developments**", *[f"- {d}" for d in history.key_developments]])
        content_parts.extend(["", "**Impact**", history.impact])
        if history.source_citations:
            sources = "\n".join(f"- {c.authors} ({c.year}). {c.title}. {c.journal}." for c in history.source_citations)
            content_parts.extend(["", "**Sources**", sources])
        _save_if_requested(args, f"History: {equation.name}", equation.equation, {
            "History": "\n".join(content_parts),
        })


def derivation_equation(args: argparse.Namespace) -> None:
    if not getattr(args, "_quiet", False):
        print_header("Equation Derivation", subtitle="The mathematical derivation of a physics equation.")
    logger.info("Fetching derivation for: %s", args.equation_name)
    explainer = _make_explainer(args)
    equation = _build_equation(args)
    derivation = explainer.get_derivation(equation)

    print_section("Equation", f"[bold]{equation.name}[/bold]\n{equation.equation}")
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

    if hasattr(args, "output") and args.output:
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
            content_dict["Limitations"] = "\n".join(f"- {x}" for x in derivation.limitations)
        _save_if_requested(args, f"Derivation: {equation.name}", equation.equation, content_dict)


def version(args: argparse.Namespace) -> None:
    print_header(f"MathEqs v{VERSION}", subtitle="Physics Equation Explainer with AI.")
    print_text("\n[bold]Available Commands[/bold]", style="")
    print_text(
        "  analyze     - Comprehensive analysis (4 sections: Intro, History, Derivation, Applications)\n"
        "  explain     - Explain a physics equation\n"
        "  history     - View equation history\n"
        "  derivation  - View equation derivation\n"
        "  list        - List sample equations\n"
        "  version     - Show version",
        style="cyan",
    )


class CLIError(Exception):
    pass


def comprehensive_equation_analysis(args: argparse.Namespace) -> None:
    print_header("Comprehensive Equation Analysis", subtitle="A complete analysis of a physics equation.")
    explainer = _make_explainer(args)
    equation = _build_equation(args)
    print_text(f"[bold]Equation:[/bold] {equation.name} — {equation.equation}", style="")
    print_text("")

    introduction_content = ""
    history_content = ""
    derivation_content = ""
    applications_content = ""

    print_text("⏳ Generating explanation...", style="cyan")
    logger.info("Generating explanation for %s", args.equation_name)
    try:
        explanation = explainer.explain_equation(equation)
        introduction_content = (
            f"**Simple Explanation:** {explanation.simple_explanation}\n\n"
            f"**Detailed Explanation:** {explanation.detailed_explanation}"
        )
        applications_content = explanation.real_world_example
        print_text("✓ Explanation generated", style="green")
    except Exception as e:
        logger.warning("Could not generate explanation: %s", e)
        print_text(f"⚠️  Could not generate explanation: {str(e)}", style="yellow")

    print_text("⏳ Generating history...", style="cyan")
    logger.info("Generating history for %s", args.equation_name)
    try:
        history = explainer.get_history(equation)
        history_content = (
            f"**Discoverer:** {history.discoverer} ({_format_year(history.year_discovered)})\n\n"
            f"**Historical Context:** {history.historical_context}\n\n"
            f"**Impact:** {history.impact}"
        )
        if history.key_developments:
            history_content += "\n\n**Key Developments:**\n" + "\n".join(f"- {d}" for d in history.key_developments)
        print_text("✓ History generated", style="green")
    except Exception as e:
        logger.warning("Could not generate history: %s", e)
        print_text(f"⚠️  Could not generate history: {str(e)}", style="yellow")

    print_text("⏳ Generating derivation...", style="cyan")
    logger.info("Generating derivation for %s", args.equation_name)
    try:
        derivation = explainer.get_derivation(equation)
        steps_text = "\n\n".join(
            f"**Step {s.step_number}: {s.title}**\n{s.description}"
            + (f"\n\n{s.mathematical_expression}" if s.mathematical_expression else "")
            for s in derivation.derivation_steps
        )
        derivation_content = (
            "**Starting Principles:**\n" + "\n".join(f"- {p}" for p in derivation.starting_principles)
            + f"\n\n**Derivation Steps:**\n{steps_text}"
        )
        print_text("✓ Derivation generated", style="green")
    except Exception as e:
        logger.warning("Could not generate derivation: %s", e)
        print_text(f"⚠️  Could not generate derivation: {str(e)}", style="yellow")

    if hasattr(args, "output") and args.output:
        markdown_content = generate_four_section_markdown(
            equation_name=args.equation_name,
            equation=equation.equation,
            introduction=introduction_content,
            history=history_content,
            derivation=derivation_content,
            applications=applications_content,
        )
        filepath = save_markdown_file(markdown_content, args.output)
        print_text(f"\n✓ Complete analysis saved to: {filepath}", style="green")
    else:
        print_section("Introduction", introduction_content)
        print_section("History", history_content)
        print_section("Derivation", derivation_content)
        print_section("Applications", applications_content)


_KNOWN_COMMANDS = ["explain", "history", "derivation", "analyze", "list", "version"]


def _parse_global_flags() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-d", "--difficulty", choices=["beginner", "intermediate", "advanced"], default="intermediate")
    parser.add_argument("-m", "--model", default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("-o", "--output", default=None)
    parser.add_argument("-c", "--context", default=None)
    args, _ = parser.parse_known_args()
    return args


def handle_equation_input(equation_name: str, global_args: argparse.Namespace) -> None:
    base = dict(
        equation=equation_name, name=None, context=global_args.context,
        output=global_args.output, model=global_args.model, seed=global_args.seed,
    )
    print_header("Physics Equation Analysis", subtitle="A complete analysis of a physics equation.")
    print_text(f"[bold]Equation:[/bold] {equation_name}\n", style="")

    print_text("[1/3] Explaining the equation...", style="cyan")
    args = argparse.Namespace(**base, difficulty=global_args.difficulty)
    explain_equation(args)

    print_text("\n[2/3] Fetching historical information...", style="cyan")
    args2 = argparse.Namespace(**base, equation_name=equation_name, difficulty=None, _quiet=True)
    history_equation(args2)

    print_text("\n[3/3] Fetching mathematical derivation...", style="cyan")
    args3 = argparse.Namespace(**base, equation_name=equation_name, difficulty=None, _quiet=True)
    derivation_equation(args3)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="matheqs",
        description="MathEqs - AI-powered physics equation explainer. Supports any litellm-compatible model.",
        epilog="Examples:\n"
        "  python cli.py 'Wave Equation'\n"
        "  python cli.py analyze 'E = mc²' -o einstein.md\n"
        "  python cli.py -m gpt-4o explain 'F = ma'\n"
        '  python cli.py history "Newton\'s Second Law"\n'
        '  python cli.py derivation "Schrödinger\'s Equation"\n'
        "  python cli.py list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-m", "--model",
        default=None,
        help="LLM model identifier in litellm format (e.g. 'gemini/gemini-2.5-flash', 'gpt-4o')",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducible LLM outputs (if supported by the provider)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    explain_parser = subparsers.add_parser("explain", help="Explain an equation")
    explain_parser.add_argument("equation", help="Physics equation to explain (e.g., 'F = ma')")
    explain_parser.add_argument("-n", "--name", help="Name of the equation")
    explain_parser.add_argument("-c", "--context", help="Additional context about the equation")
    explain_parser.add_argument(
        "-d", "--difficulty",
        choices=["beginner", "intermediate", "advanced"],
        default="intermediate",
        help="Difficulty level (default: intermediate)",
    )
    explain_parser.add_argument("-o", "--output", metavar="FILE", help="Save output to Markdown file")
    explain_parser.set_defaults(func=explain_equation)

    history_parser = subparsers.add_parser("history", help="View equation history")
    history_parser.add_argument("equation_name", help="Name of the equation")
    history_parser.add_argument("-c", "--context", help="Additional context about the equation")
    history_parser.add_argument(
        "-d", "--difficulty",
        choices=["beginner", "intermediate", "advanced"],
        help="Difficulty level",
    )
    history_parser.add_argument("-o", "--output", metavar="FILE", help="Save output to Markdown file")
    history_parser.set_defaults(func=history_equation)

    derivation_parser = subparsers.add_parser("derivation", help="View equation derivation")
    derivation_parser.add_argument("equation_name", help="Name of the equation")
    derivation_parser.add_argument("-c", "--context", help="Additional context about the equation")
    derivation_parser.add_argument(
        "-d", "--difficulty",
        choices=["beginner", "intermediate", "advanced"],
        help="Difficulty level",
    )
    derivation_parser.add_argument("-o", "--output", metavar="FILE", help="Save output to Markdown file")
    derivation_parser.set_defaults(func=derivation_equation)

    analyze_parser = subparsers.add_parser(
        "analyze", help="Comprehensive analysis with 4 sections: Introduction, History, Derivation, Applications"
    )
    analyze_parser.add_argument("equation_name", help="Name of the equation")
    analyze_parser.add_argument("-c", "--context", help="Additional context about the equation")
    analyze_parser.add_argument(
        "-d", "--difficulty",
        choices=["beginner", "intermediate", "advanced"],
        default="intermediate",
        help="Difficulty level (default: intermediate)",
    )
    analyze_parser.add_argument("-o", "--output", metavar="FILE", help="Save output to Markdown file")
    analyze_parser.set_defaults(func=comprehensive_equation_analysis)

    list_parser = subparsers.add_parser("list", help="List sample equations")
    list_parser.set_defaults(func=list_equations)

    version_parser = subparsers.add_parser("version", help="Show version")
    version_parser.set_defaults(func=version)

    return parser


def _configure_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def main() -> None:
    _configure_logging()

    global_args = _parse_global_flags()
    _check_api_key(global_args.model)

    try:
        if len(sys.argv) > 1 and sys.argv[1] not in _KNOWN_COMMANDS and not sys.argv[1].startswith("-"):
            equation_name = sys.argv[1]
            handle_equation_input(equation_name, global_args)
            return

        parser = create_parser()
        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return

        args.func(args)
    except CLIError as e:
        logger.error(str(e))
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
