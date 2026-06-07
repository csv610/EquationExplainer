import logging
import time
from typing import TypeVar, cast

import litellm

from models import (
    DerivationModel,
    EquationExplanation,
    EquationModel,
    HistoryModel,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")

_PSEUDOSCIENCE_KEYWORDS = [
    "perpetual motion", "free energy", "overunity", "tachyons",
    "orgone", "zero-point energy", "cold fusion", "phlogiston",
    "ether", "antigravity", "psychic", "telepathy",
]

SYSTEM_PROMPTS = {
    "explain": (
        "You are an expert physics teacher. Explain equations clearly and accurately."
        " Structure your response to be pedagogically sound."
        " When applicable, note the limits of the equation and common misconceptions."
        " Always clarify which quantities are variable names vs. constants."
    ),
    "history": (
        "You are a physics historian with a PhD in history of science."
        " Provide accurate historical context for physics equations."
        " Include specific dates, publications, and the broader scientific milieu."
        " If the historical record is contested or uncertain, acknowledge this."
        " Always cite specific publications (title, journal, year) where discoveries were first presented."
        " Distinguish between the equation's discoverer and earlier contributors who laid groundwork."
    ),
    "derivation": (
        "You are a physics professor deriving equations step-by-step."
        " Use clear mathematical reasoning at each step."
        " State which physical principles or mathematical techniques justify each transformation."
        " Include the domain of validity and assumptions at each step."
        " Note when a step relies on approximation rather than exact equality."
    ),
}


def _check_pseudoscience(equation: EquationModel) -> list[str]:
    combined = f"{equation.name} {equation.equation}".lower()
    return [kw for kw in _PSEUDOSCIENCE_KEYWORDS if kw in combined]


class PhysicsEquationExplainer:

    def __init__(
        self,
        model: str = "ollama/gemma4",
        temperature: float = 0.7,
        seed: int | None = None,
        max_retries: int = 3,
    ):
        self.model = model
        self.temperature = temperature
        self.seed = seed
        self.max_retries = max_retries

    def __repr__(self) -> str:
        parts = [f"model={self.model!r}", f"temperature={self.temperature}"]
        if self.seed is not None:
            parts.append(f"seed={self.seed}")
        return f"PhysicsEquationExplainer({', '.join(parts)})"

    def _build_prompt(self, equation: EquationModel, task: str) -> str:
        parts = [f"# {task.capitalize()} of: {equation.name}"]
        parts.append(f"$$ {equation.equation} $$")
        if equation.context:
            parts.append(f"\n**Context:** {equation.context}")
        if equation.difficulty:
            parts.append(f"\n**Target audience:** {equation.difficulty}")
        parts.append(
            "\n---\n"
            "**Instructions:**\n"
            "- Be precise and rigorous. Use proper mathematical notation.\n"
            "- If the equation is incorrectly stated, note the correction.\n"
            "- Distinguish between fundamental laws and derived results.\n"
            "- Mention the domain of validity.\n"
            "- For historical claims, cite specific publications.\n"
            "- Acknowledge uncertainty where the literature is contested."
        )
        return "\n".join(parts)

    def _call_llm(self, content: str, system_prompt: str, response_model: type[T]) -> T:
        kwargs = dict(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content},
            ],
            temperature=self.temperature,
            response_format=response_model,
        )
        if self.seed is not None:
            kwargs["seed"] = self.seed

        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info("LLM call attempt %d/%d model=%s", attempt, self.max_retries, self.model)
                response = litellm.completion(**kwargs)
                if not response.choices:
                    raise RuntimeError("LLM returned no choices")
                parsed = response.choices[0].message.parsed
                if parsed is None:
                    raise RuntimeError("LLM returned no parsed response")
                logger.info("LLM call successful on attempt %d", attempt)
                return cast(T, parsed)
            except litellm.AuthenticationError as e:
                raise RuntimeError(
                    f"Authentication failed for model '{self.model}'. "
                    "Check your API key is set correctly in .env or environment variables. "
                    f"Error: {e}"
                ) from e
            except litellm.RateLimitError as e:
                wait = min(2 ** attempt, 30)
                logger.warning("Rate limited, retrying in %ds (attempt %d)", wait, attempt)
                time.sleep(wait)
                last_error = e
            except (litellm.APIConnectionError, litellm.ServiceUnavailableError) as e:
                wait = min(2 ** attempt, 30)
                logger.warning("API unavailable, retrying in %ds (attempt %d)", wait, attempt)
                time.sleep(wait)
                last_error = e
            except litellm.Timeout as e:
                wait = min(2 ** attempt, 30)
                logger.warning("API timeout, retrying in %ds (attempt %d)", wait, attempt)
                time.sleep(wait)
                last_error = e
            except Exception as e:
                last_error = e
                if attempt == self.max_retries:
                    raise RuntimeError(
                        f"LLM call failed after {self.max_retries} attempts. "
                        f"Model: {self.model}. "
                        f"Error: {e}"
                    ) from e

        raise RuntimeError(
            f"LLM call failed after {self.max_retries} attempts. "
            f"Model: {self.model}. "
            f"Last error: {last_error}"
        ) from last_error

    def _call_with_overrides(
        self, equation: EquationModel, response_model: type[T], task: str
    ) -> T:
        warnings = _check_pseudoscience(equation)
        if warnings:
            logger.warning(
                "Equation matched pseudoscience keywords: %s. Proceeding anyway.", warnings
            )
        prompt = self._build_prompt(equation, task)
        system_prompt = SYSTEM_PROMPTS.get(task, SYSTEM_PROMPTS["explain"])
        return self._call_llm(prompt, system_prompt, response_model)

    def explain_equation(self, equation: EquationModel) -> EquationExplanation:
        return self._call_with_overrides(equation, EquationExplanation, "explain")

    def get_history(self, equation: EquationModel) -> HistoryModel:
        return self._call_with_overrides(equation, HistoryModel, "history")

    def get_derivation(self, equation: EquationModel) -> DerivationModel:
        return self._call_with_overrides(equation, DerivationModel, "derivation")

    @staticmethod
    def get_available_equations() -> list[str]:
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

    @staticmethod
    def get_pseudoscience_keywords() -> list[str]:
        return list(_PSEUDOSCIENCE_KEYWORDS)
