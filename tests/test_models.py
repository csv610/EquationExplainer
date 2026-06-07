"""Tests for Pydantic models"""
import pytest
from models import (
    PhysicsEquation,
    EquationExplanation,
    HistoryModel,
    ApplicationModel,
    DerivationStep,
    DerivationModel,
    EquationModel,
)


class TestPhysicsEquation:
    """Tests for PhysicsEquation model"""

    def test_create_basic_equation(self):
        """Test creating a basic physics equation"""
        eq = PhysicsEquation(
            name="Newton's Second Law",
            equation="F = ma"
        )
        assert eq.name == "Newton's Second Law"
        assert eq.equation == "F = ma"
        assert eq.context is None
        assert eq.variables is None

    def test_create_equation_with_all_fields(self):
        """Test creating equation with all fields"""
        eq = PhysicsEquation(
            name="Newton's Second Law",
            equation="F = ma",
            context="Classical mechanics",
            variables={"F": "Force", "m": "mass", "a": "acceleration"}
        )
        assert eq.name == "Newton's Second Law"
        assert eq.equation == "F = ma"
        assert eq.context == "Classical mechanics"
        assert len(eq.variables) == 3
        assert eq.variables["F"] == "Force"

    def test_equation_requires_name(self):
        """Test that name is required"""
        with pytest.raises(ValueError):
            PhysicsEquation(equation="F = ma")

    def test_equation_requires_equation(self):
        """Test that equation is required"""
        with pytest.raises(ValueError):
            PhysicsEquation(name="Newton's Second Law")


class TestEquationExplanation:
    """Tests for EquationExplanation model"""

    def test_create_full_explanation(self):
        """Test creating a complete equation explanation"""
        exp = EquationExplanation(
            equation_name="Newton's Second Law",
            equation="F = ma",
            simple_explanation="Force equals mass times acceleration",
            detailed_explanation="Newton's second law states that the net force on an object is equal to the mass of the object multiplied by its acceleration.",
            real_world_example="When you push a car, the harder you push, the faster it accelerates.",
            key_concepts=["force", "mass", "acceleration"]
        )
        assert exp.equation_name == "Newton's Second Law"
        assert exp.equation == "F = ma"
        assert len(exp.key_concepts) == 3

    def test_requires_all_fields(self):
        """Test that all fields are required"""
        with pytest.raises(ValueError):
            EquationExplanation(
                equation_name="Test",
                equation="E = mc²"
            )


class TestEquationModel:
    """Tests for EquationModel"""

    def test_create_minimal(self):
        """Test creating with only required fields"""
        model = EquationModel(name="Test", equation="F = ma")
        assert model.name == "Test"
        assert model.equation == "F = ma"
        assert model.context is None
        assert model.difficulty is None

    def test_create_with_all_fields(self):
        """Test creating with all fields"""
        model = EquationModel(
            name="Test",
            equation="F = ma",
            context="Classical mechanics",
            difficulty="beginner"
        )
        assert model.context == "Classical mechanics"
        assert model.difficulty == "beginner"

    def test_equation_is_required(self):
        """Test that equation field is required"""
        with pytest.raises(ValueError):
            EquationModel(name="Test")

    def test_name_is_required(self):
        """Test that name is required"""
        with pytest.raises(ValueError):
            EquationModel(equation="F = ma")


class TestHistoryModel:
    """Tests for HistoryModel"""

    def test_create_minimal(self):
        """Test creating a minimal history"""
        history = HistoryModel(
            equation_name="Newton's Second Law",
            equation="F = ma",
            year_discovered=1687,
            discoverer="Isaac Newton",
            historical_context="Developed during the Scientific Revolution",
            impact="Foundation of classical mechanics"
        )
        assert history.equation_name == "Newton's Second Law"
        assert history.equation == "F = ma"
        assert history.year_discovered == 1687
        assert history.discoverer == "Isaac Newton"
        assert history.earlier_related_equations is None
        assert history.key_developments is None

    def test_create_with_developments(self):
        """Test creating history with developments"""
        history = HistoryModel(
            equation_name="Einstein's Mass-Energy Equivalence",
            equation="E = mc²",
            year_discovered=1905,
            discoverer="Albert Einstein",
            historical_context="Developed as part of special relativity",
            earlier_related_equations=[
                "Conservation of energy",
                "Lorentz transformations",
                "Maxwell's equations"
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
            ]
        )
        assert history.year_discovered == 1905
        assert len(history.earlier_related_equations) == 3
        assert len(history.key_developments) == 2
        assert len(history.applications) == 2
        assert history.country_of_origin == "Switzerland (Bern)"

    def test_required_fields(self):
        """Test that required fields must be provided"""
        with pytest.raises(ValueError):
            HistoryModel(
                equation_name="Test",
                year_discovered=2000
            )

    def test_year_discovered_type(self):
        """Test that year_discovered is an integer"""
        history = HistoryModel(
            equation_name="Test Law",
            equation="a = b",
            year_discovered=1800,
            discoverer="Test Scientist",
            historical_context="Test context",
            impact="Test impact"
        )
        assert isinstance(history.year_discovered, int)
        assert history.year_discovered == 1800

    def test_optional_fields_are_truly_optional(self):
        """Test that optional fields can be omitted"""
        history = HistoryModel(
            equation_name="Simple Law",
            equation="x = y",
            year_discovered=1999,
            discoverer="Someone",
            historical_context="Some context",
            impact="Some impact"
        )
        assert history.earlier_related_equations is None
        assert history.key_developments is None
        assert history.original_publication is None
        assert history.country_of_origin is None
        assert history.competing_theories is None
        assert history.applications is None

    def test_key_developments_as_timeline(self):
        """Test that key_developments works as a timeline"""
        history = HistoryModel(
            equation_name="Evolution Test",
            equation="a + b = c",
            year_discovered=1800,
            discoverer="Test",
            historical_context="Test",
            impact="Test",
            key_developments=[
                "1800: Initial discovery",
                "1850: First refinement",
                "1900: Major breakthrough",
                "2000: Modern applications"
            ]
        )
        assert len(history.key_developments) == 4
        assert "1800" in history.key_developments[0]
        assert "2000" in history.key_developments[3]


class TestDerivationStep:
    """Tests for DerivationStep model"""

    def test_create_derivation_step(self):
        """Test creating a single derivation step"""
        step = DerivationStep(
            step_number=1,
            title="Apply Newton's Second Law",
            description="Start with the fundamental law F = ma",
            mathematical_expression="F = m * a",
            reasoning="Foundation of classical mechanics"
        )
        assert step.step_number == 1
        assert step.title == "Apply Newton's Second Law"
        assert "F = m * a" in step.mathematical_expression

    def test_derivation_step_with_equations(self):
        """Test derivation step with before and after equations"""
        step = DerivationStep(
            step_number=3,
            title="Simplification",
            description="Combine like terms and simplify",
            mathematical_expression="Divide both sides by (a-b)",
            reasoning="Isolate the variable of interest",
            from_equation="2x(a-b) = c(a-b)",
            to_equation="2x = c"
        )
        assert step.from_equation == "2x(a-b) = c(a-b)"
        assert step.to_equation == "2x = c"
        assert step.step_number == 3


class TestDerivationModel:
    """Tests for DerivationModel"""

    def test_create_minimal(self):
        """Test creating derivation with only required fields"""
        derivation = DerivationModel(
            equation_name="Kinetic Energy",
            equation="KE = (1/2)mv²",
            starting_principles=[
                "Work-energy theorem",
                "Newton's laws of motion"
            ],
            derivation_steps=[
                DerivationStep(
                    step_number=1,
                    title="Define kinetic energy",
                    description="Energy due to motion",
                    mathematical_expression="KE = W",
                    reasoning="Definition"
                )
            ]
        )
        assert derivation.equation_name == "Kinetic Energy"
        assert len(derivation.starting_principles) == 2
        assert len(derivation.derivation_steps) == 1

    def test_complete_derivation(self):
        """Test complete derivation with all fields"""
        derivation = DerivationModel(
            equation_name="Fourier's Law of Heat Conduction",
            equation="Q/t = -kA(dT/dx)",
            starting_principles=[
                "Energy conservation",
                "Experimental observation of heat flow",
            ],
            derivation_steps=[
                DerivationStep(
                    step_number=1,
                    title="Energy Balance",
                    description="Apply first law of thermodynamics",
                    mathematical_expression="dQ_in - dQ_out = dE_stored/dt",
                    reasoning="Conservation of energy",
                ),
            ],
            alternative_derivations=[
                "From molecular transport theory",
                "From Boltzmann transport equation"
            ],
            special_cases=[
                "Constant temperature case: Q/t = 0",
                "Uniform temperature gradient"
            ],
            validity_conditions=[
                "Steady-state heat transfer",
                "Constant thermal conductivity",
            ],
            limitations=[
                "Breaks down at very high temperature gradients",
                "Not valid for non-Fourier heat conduction",
            ],
            extensions_generalizations=[
                "Three-dimensional form: q = -k∇T",
                "Transient heat conduction",
            ],
            mathematical_prerequisites=[
                "Partial derivatives",
                "Differential equations",
            ],
            related_equations=[
                "Heat diffusion equation",
                "Thermal resistance",
            ]
        )
        assert len(derivation.starting_principles) == 2
        assert len(derivation.derivation_steps) == 1
        assert len(derivation.alternative_derivations) == 2
        assert len(derivation.special_cases) == 2
        assert len(derivation.validity_conditions) == 2
        assert len(derivation.limitations) == 2
        assert len(derivation.extensions_generalizations) == 2
        assert len(derivation.mathematical_prerequisites) == 2
        assert len(derivation.related_equations) == 2
