"""Tests for Pydantic models"""
import pytest

from models import (
    ApplicationModel,
    DerivationModel,
    DerivationStep,
    EquationExplanation,
    EquationModel,
    HistoryModel,
    SourceCitation,
)


class TestEquationModel:

    def test_create_basic_equation(self):
        eq = EquationModel(name="Newton's Second Law", equation="F = ma")
        assert eq.name == "Newton's Second Law"
        assert eq.equation == "F = ma"
        assert eq.context is None

    def test_create_equation_with_context(self):
        eq = EquationModel(
            name="Newton's Second Law",
            equation="F = ma",
            context="Classical mechanics",
        )
        assert eq.context == "Classical mechanics"

    def test_equation_requires_name(self):
        with pytest.raises(ValueError):
            EquationModel(equation="F = ma")

    def test_equation_requires_equation(self):
        with pytest.raises(ValueError):
            EquationModel(name="Newton's Second Law")

    def test_create_minimal(self):
        model = EquationModel(name="Test", equation="F = ma")
        assert model.difficulty is None

    def test_create_with_all_optional(self):
        model = EquationModel(name="Test", equation="F = ma", difficulty="beginner")
        assert model.difficulty == "beginner"

    def test_extra_fields_are_forbidden(self):
        with pytest.raises(ValueError, match="Extra inputs are not permitted"):
            EquationModel(name="Test", equation="x=y", extra_field="bad")


class TestEquationExplanation:

    def test_create_full_explanation(self):
        exp = EquationExplanation(
            simple_explanation="Force equals mass times acceleration",
            detailed_explanation="Newton's second law states that the net force on an object is equal to the mass of the object multiplied by its acceleration.",
            real_world_example="When you push a car, the harder you push, the faster it accelerates.",
            key_concepts=["force", "mass", "acceleration"],
        )
        assert len(exp.key_concepts) == 3

    def test_requires_all_fields(self):
        with pytest.raises(ValueError):
            EquationExplanation(simple_explanation="test", detailed_explanation="test")

    def test_extra_fields_are_forbidden(self):
        with pytest.raises(ValueError, match="Extra inputs are not permitted"):
            EquationExplanation(
                simple_explanation="a", detailed_explanation="b",
                real_world_example="c", key_concepts=[], bad_field="x",
            )


class TestHistoryModel:

    def test_create_minimal(self):
        history = HistoryModel(
            year_discovered=1687,
            discoverer="Isaac Newton",
            historical_context="Developed during the Scientific Revolution",
            impact="Foundation of classical mechanics",
        )
        assert history.year_discovered == 1687
        assert history.discoverer == "Isaac Newton"
        assert history.earlier_related_equations is None
        assert history.source_citations == []

    def test_create_with_developments(self):
        history = HistoryModel(
            year_discovered=1905,
            discoverer="Albert Einstein",
            historical_context="Developed as part of special relativity",
            earlier_related_equations=[
                "Conservation of energy", "Lorentz transformations", "Maxwell's equations",
            ],
            key_developments=[
                "1905: Initial publication in 'On the Electrodynamics of Moving Bodies'",
                "1907: Extension to general relativity",
            ],
            impact="Revolutionized understanding of energy and matter",
            original_publication="Annalen der Physik, 1905",
            country_of_origin="Switzerland (Bern)",
            competing_theories=["Ether theory", "Newtonian mechanics"],
            applications=[
                ApplicationModel(title="Nuclear power", description="Nuclear power generation"),
                ApplicationModel(title="PET scans", description="Medical imaging"),
            ],
            source_citations=[
                SourceCitation(
                    title="On the Electrodynamics of Moving Bodies",
                    authors="Albert Einstein",
                    year=1905,
                    journal="Annalen der Physik",
                ),
            ],
        )
        assert len(history.earlier_related_equations) == 3
        assert len(history.key_developments) == 2
        assert len(history.applications) == 2
        assert len(history.source_citations) == 1

    def test_required_fields(self):
        with pytest.raises(ValueError):
            HistoryModel(equation_name="Test", year_discovered=2000)

    def test_optional_fields_are_truly_optional(self):
        history = HistoryModel(
            year_discovered=1999,
            discoverer="Someone",
            historical_context="Some context",
            impact="Some impact",
        )
        assert history.earlier_related_equations is None
        assert history.key_developments is None
        assert history.original_publication is None
        assert history.country_of_origin is None
        assert history.competing_theories is None
        assert history.applications is None
        assert history.source_citations == []

    def test_extra_fields_are_forbidden(self):
        with pytest.raises(ValueError, match="Extra inputs are not permitted"):
            HistoryModel(
                year_discovered=2000, discoverer="X", historical_context="X",
                impact="X", bad=True,
            )


class TestSourceCitation:

    def test_create_citation(self):
        cite = SourceCitation(
            title="On the Electrodynamics of Moving Bodies",
            authors="Albert Einstein",
            year=1905,
            journal="Annalen der Physik",
        )
        assert cite.title == "On the Electrodynamics of Moving Bodies"
        assert cite.url is None

    def test_citation_with_url(self):
        cite = SourceCitation(
            title="Test",
            authors="Author",
            year=2020,
            journal="Journal",
            url="https://example.com",
        )
        assert cite.url == "https://example.com"

    def test_extra_fields_are_forbidden(self):
        with pytest.raises(ValueError, match="Extra inputs are not permitted"):
            SourceCitation(
                title="T", authors="A", year=2020, journal="J", bad=True,
            )


class TestDerivationStep:

    def test_create_derivation_step(self):
        step = DerivationStep(
            step_number=1,
            title="Apply Newton's Second Law",
            description="Start with the fundamental law F = ma",
            mathematical_expression="F = m * a",
            reasoning="Foundation of classical mechanics",
        )
        assert step.step_number == 1
        assert step.title == "Apply Newton's Second Law"

    def test_derivation_step_with_equations(self):
        step = DerivationStep(
            step_number=3,
            title="Simplification",
            description="Combine like terms and simplify",
            mathematical_expression="Divide both sides by (a-b)",
            reasoning="Isolate the variable of interest",
            from_equation="2x(a-b) = c(a-b)",
            to_equation="2x = c",
        )
        assert step.from_equation == "2x(a-b) = c(a-b)"
        assert step.to_equation == "2x = c"


class TestDerivationModel:

    def test_create_minimal(self):
        derivation = DerivationModel(
            starting_principles=["Work-energy theorem", "Newton's laws of motion"],
            derivation_steps=[
                DerivationStep(
                    step_number=1, title="Define kinetic energy",
                    description="Energy due to motion",
                    mathematical_expression="KE = W",
                    reasoning="Definition",
                )
            ],
        )
        assert len(derivation.starting_principles) == 2
        assert len(derivation.derivation_steps) == 1

    def test_complete_derivation(self):
        derivation = DerivationModel(
            starting_principles=["Energy conservation", "Experimental observation of heat flow"],
            derivation_steps=[
                DerivationStep(
                    step_number=1, title="State the principle",
                    description="Energy cannot be created or destroyed",
                    mathematical_expression="ΔU = Q - W",
                    reasoning="First law of thermodynamics",
                ),
                DerivationStep(
                    step_number=2, title="Apply to heat conduction",
                    description="Consider heat flow through a material",
                    mathematical_expression="q = -k∇T",
                    reasoning="Fourier's law of heat conduction",
                ),
            ],
            mathematical_prerequisites=["Calculus", "Partial differential equations"],
            validity_conditions=["Isotropic material", "Constant thermal conductivity"],
            limitations=["Does not account for convection", "Steady-state only"],
            alternative_derivations=["Statistical mechanics approach"],
            special_cases=["One-dimensional heat flow: d²T/dx² = 0"],
            extensions_generalizations=["Including heat generation term"],
            related_equations=["Diffusion equation", "Wave equation"],
        )
        assert len(derivation.derivation_steps) == 2
        assert len(derivation.mathematical_prerequisites) == 2
        assert len(derivation.validity_conditions) == 2
        assert len(derivation.limitations) == 2
        assert len(derivation.alternative_derivations) == 1
        assert len(derivation.special_cases) == 1
        assert len(derivation.extensions_generalizations) == 1
        assert len(derivation.related_equations) == 2

    def test_extra_fields_are_forbidden(self):
        with pytest.raises(ValueError, match="Extra inputs are not permitted"):
            DerivationModel(
                starting_principles=["Test"],
                derivation_steps=[
                    DerivationStep(
                        step_number=1, title="T", description="D",
                        mathematical_expression="E", reasoning="R",
                    )
                ],
                invalid=True,
            )


class TestApplicationModel:

    def test_create_application(self):
        app = ApplicationModel(title="Nuclear Power", description="Energy generation")
        assert app.title == "Nuclear Power"
        assert app.description == "Energy generation"

    def test_extra_fields_are_forbidden(self):
        with pytest.raises(ValueError, match="Extra inputs are not permitted"):
            ApplicationModel(title="T", description="D", bad=True)
