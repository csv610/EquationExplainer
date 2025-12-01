"""Tests for Pydantic models"""
import pytest
from models import (
    PhysicsEquation,
    EquationExplanation,
    ExplanationRequest,
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


class TestExplanationRequest:
    """Tests for ExplanationRequest model"""

    def test_create_minimal_request(self):
        """Test creating a request with only required field"""
        req = ExplanationRequest(equation="F = ma")
        assert req.equation == "F = ma"
        assert req.difficulty_level == "intermediate"
        assert req.equation_name is None
        assert req.context is None

    def test_create_full_request(self):
        """Test creating a request with all fields"""
        req = ExplanationRequest(
            equation="F = ma",
            equation_name="Newton's Second Law",
            context="Classical mechanics",
            difficulty_level="beginner"
        )
        assert req.equation == "F = ma"
        assert req.equation_name == "Newton's Second Law"
        assert req.context == "Classical mechanics"
        assert req.difficulty_level == "beginner"

    def test_difficulty_level_default(self):
        """Test that difficulty_level defaults to intermediate"""
        req = ExplanationRequest(equation="E = mc²")
        assert req.difficulty_level == "intermediate"

    def test_valid_difficulty_levels(self):
        """Test that various difficulty levels are accepted"""
        for level in ["beginner", "intermediate", "advanced"]:
            req = ExplanationRequest(equation="F = ma", difficulty_level=level)
            assert req.difficulty_level == level

    def test_equation_is_required(self):
        """Test that equation field is required"""
        with pytest.raises(ValueError):
            ExplanationRequest()


class TestEquationHistory:
    """Tests for EquationHistory model"""

    def test_create_minimal_history(self):
        """Test creating a minimal equation history"""
        history = EquationHistory(
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

    def test_create_full_history(self):
        """Test creating equation history with all fields"""
        history = EquationHistory(
            equation_name="Einstein's Mass-Energy Equivalence",
            equation="E = mc²",
            year_discovered=1905,
            discoverer="Albert Einstein",
            historical_context="Developed as part of special relativity theory during the Annus Mirabilis",
            earlier_related_equations=[
                "Conservation of energy",
                "Lorentz transformations",
                "Maxwell's equations"
            ],
            key_developments=[
                "1905: Initial publication in 'On the Electrodynamics of Moving Bodies'",
                "1907: Extension to general relativity",
                "1938: First experimental confirmation with nuclear fission"
            ],
            impact="Revolutionized understanding of energy and matter, leading to nuclear physics",
            original_publication="Annalen der Physik, 1905",
            country_of_origin="Switzerland (Bern)",
            competing_theories=["Ether theory", "Newtonian mechanics"],
            modern_applications=[
                "Nuclear power generation",
                "Nuclear weapons",
                "Medical imaging (PET scans)",
                "Particle accelerators"
            ]
        )
        assert history.equation_name == "Einstein's Mass-Energy Equivalence"
        assert history.year_discovered == 1905
        assert len(history.earlier_related_equations) == 3
        assert len(history.key_developments) == 3
        assert len(history.modern_applications) == 4
        assert history.country_of_origin == "Switzerland (Bern)"

    def test_required_fields(self):
        """Test that required fields must be provided"""
        with pytest.raises(ValueError):
            EquationHistory(
                equation_name="Test",
                year_discovered=2000
                # Missing: equation, discoverer, historical_context, impact
            )

    def test_year_discovered_type(self):
        """Test that year_discovered is an integer"""
        history = EquationHistory(
            equation_name="Test Law",
            equation="a = b",
            year_discovered=1800,
            discoverer="Test Scientist",
            historical_context="Test context",
            impact="Test impact"
        )
        assert isinstance(history.year_discovered, int)
        assert history.year_discovered == 1800

    def test_heat_conduction_history(self):
        """Test creating history for heat conduction equation"""
        history = EquationHistory(
            equation_name="Fourier's Law of Heat Conduction",
            equation="Q/t = -kA(dT/dx)",
            year_discovered=1822,
            discoverer="Jean-Baptiste Joseph Fourier",
            historical_context="Developed while studying heat transfer in solids during industrial revolution",
            earlier_related_equations=[
                "Newton's Law of Cooling",
                "Caloric theory of heat"
            ],
            key_developments=[
                "1822: Published in 'Théorie analytique de la chaleur'",
                "1830s: Refined mathematical framework",
                "1920s: Quantum mechanical explanation"
            ],
            impact="Foundation of thermodynamics and heat transfer engineering",
            original_publication="Théorie analytique de la chaleur, 1822",
            country_of_origin="France",
            competing_theories=[
                "Caloric theory",
                "Radiation-only heat transfer"
            ],
            modern_applications=[
                "HVAC system design",
                "Heat exchanger engineering",
                "Thermal insulation optimization",
                "Electronics cooling",
                "Geothermal energy"
            ]
        )
        assert history.year_discovered == 1822
        assert history.discoverer == "Jean-Baptiste Joseph Fourier"
        assert "Jean-Baptiste Joseph Fourier" in history.discoverer
        assert len(history.modern_applications) == 5
        assert history.country_of_origin == "France"

    def test_optional_fields_are_truly_optional(self):
        """Test that optional fields can be omitted"""
        history = EquationHistory(
            equation_name="Simple Law",
            equation="x = y",
            year_discovered=1999,
            discoverer="Someone",
            historical_context="Some context",
            impact="Some impact"
            # All optional fields omitted
        )
        assert history.earlier_related_equations is None
        assert history.key_developments is None
        assert history.original_publication is None
        assert history.country_of_origin is None
        assert history.competing_theories is None
        assert history.modern_applications is None

    def test_key_developments_as_timeline(self):
        """Test that key_developments works as a timeline"""
        history = EquationHistory(
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

    def test_heat_conduction_step(self):
        """Test derivation step for heat conduction"""
        step = DerivationStep(
            step_number=2,
            title="Apply Energy Conservation",
            description="Heat flow into surface equals heat flow out plus energy stored",
            mathematical_expression="dQ_in/dt = dQ_out/dt + dE_stored/dt",
            reasoning="First law of thermodynamics",
            from_equation="Energy balance",
            to_equation="Fourier's law representation"
        )
        assert "Energy Conservation" in step.title
        assert "thermodynamics" in step.reasoning


class TestEquationDerivation:
    """Tests for EquationDerivation model"""

    def test_create_minimal_derivation(self):
        """Test creating derivation with only required fields"""
        derivation = EquationDerivation(
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

    def test_heat_conduction_derivation(self):
        """Test complete derivation for heat conduction equation"""
        derivation = EquationDerivation(
            equation_name="Fourier's Law of Heat Conduction",
            equation="Q/t = -kA(dT/dx)",
            starting_principles=[
                "Energy conservation",
                "Experimental observation of heat flow",
                "Continuity equation"
            ],
            derivation_steps=[
                DerivationStep(
                    step_number=1,
                    title="Energy Balance",
                    description="Apply first law of thermodynamics to a thin element",
                    mathematical_expression="dQ_in - dQ_out = dE_stored/dt",
                    reasoning="Conservation of energy",
                    to_equation="Heat flux definition"
                ),
                DerivationStep(
                    step_number=2,
                    title="Define Heat Flux",
                    description="Heat flux is rate of heat transfer per unit area",
                    mathematical_expression="q = Q/(A*t)",
                    reasoning="Definition of flux",
                    to_equation="Heat flow rate equation"
                ),
                DerivationStep(
                    step_number=3,
                    title="Experimental Observation",
                    description="Heat flux is proportional to temperature gradient",
                    mathematical_expression="q ∝ dT/dx",
                    reasoning="Fourier's experimental findings",
                    to_equation="Proportionality becomes Fourier's law"
                ),
                DerivationStep(
                    step_number=4,
                    title="Introduce Thermal Conductivity",
                    description="Define k as proportionality constant",
                    mathematical_expression="q = -k(dT/dx)",
                    reasoning="Material property definition",
                    from_equation="q ∝ dT/dx",
                    to_equation="Fourier's law (heat flux form)"
                ),
                DerivationStep(
                    step_number=5,
                    title="Total Heat Flow Rate",
                    description="Multiply heat flux by surface area",
                    mathematical_expression="Q/t = q * A",
                    reasoning="Total flow = flux density × area",
                    from_equation="q = -k(dT/dx)",
                    to_equation="Q/t = -kA(dT/dx)"
                )
            ],
            alternative_derivations=[
                "From molecular transport theory (kinetic theory)",
                "From statistical mechanics and phonon transport",
                "From Boltzmann transport equation"
            ],
            special_cases=[
                "Constant temperature case: Q/t = 0",
                "Uniform temperature gradient: dT/dx = ΔT/L",
                "Spherical geometry: Q/t = 4πkr₁r₂(T₁-T₂)/(r₂-r₁)"
            ],
            validity_conditions=[
                "Steady-state heat transfer",
                "Constant thermal conductivity",
                "No heat generation in the medium",
                "Well-defined temperature gradient"
            ],
            limitations=[
                "Breaks down at very high temperature gradients",
                "Assumes local thermodynamic equilibrium",
                "Not valid for non-Fourier heat conduction",
                "Fails in ballistic transport regime"
            ],
            extensions_generalizations=[
                "Three-dimensional form: q = -k∇T",
                "Transient heat conduction: ∂T/∂t = α∇²T",
                "Variable thermal conductivity: q = -k(T)∇T",
                "Anisotropic materials: tensor form of k"
            ],
            mathematical_prerequisites=[
                "Partial derivatives (∂T/∂x)",
                "Vector calculus (divergence, gradient)",
                "Differential equations",
                "Linear algebra (for tensor form)"
            ],
            related_equations=[
                "Heat diffusion equation: ∂T/∂t = α∇²T",
                "Thermal resistance: R = L/(kA)",
                "Heat capacity: Q = mcΔT",
                "Newton's law of cooling: Q/t = h*A*(T-T∞)"
            ]
        )
        assert derivation.equation_name == "Fourier's Law of Heat Conduction"
        assert len(derivation.starting_principles) == 3
        assert len(derivation.derivation_steps) == 5
        assert len(derivation.alternative_derivations) == 3
        assert len(derivation.special_cases) == 3
        assert len(derivation.validity_conditions) == 4
        assert len(derivation.limitations) == 4
        assert len(derivation.extensions_generalizations) == 4
        assert len(derivation.mathematical_prerequisites) == 4
        assert len(derivation.related_equations) == 4

    def test_newton_second_law_derivation(self):
        """Test derivation for Newton's Second Law"""
        derivation = EquationDerivation(
            equation_name="Newton's Second Law",
            equation="F = ma",
            starting_principles=[
                "Definition of momentum p = mv",
                "Newton's first law (inertia)",
                "Experimental observation of force"
            ],
            derivation_steps=[
                DerivationStep(
                    step_number=1,
                    title="Start with momentum definition",
                    description="Define linear momentum as p = mv",
                    mathematical_expression="p = m * v",
                    reasoning="Fundamental definition"
                ),
                DerivationStep(
                    step_number=2,
                    title="Apply force definition",
                    description="Force is rate of change of momentum",
                    mathematical_expression="F = dp/dt",
                    reasoning="Newton's definition of force",
                    to_equation="F = d(mv)/dt"
                ),
                DerivationStep(
                    step_number=3,
                    title="Differentiate momentum",
                    description="Apply product rule (m is constant)",
                    mathematical_expression="F = m(dv/dt) + v(dm/dt)",
                    reasoning="Product rule for differentiation"
                ),
                DerivationStep(
                    step_number=4,
                    title="Assume constant mass",
                    description="dm/dt = 0 for constant mass objects",
                    mathematical_expression="F = m(dv/dt)",
                    reasoning="Valid for most classical mechanics",
                    from_equation="F = m(dv/dt) + v(dm/dt)",
                    to_equation="F = m(dv/dt)"
                ),
                DerivationStep(
                    step_number=5,
                    title="Recognize acceleration",
                    description="Acceleration is rate of change of velocity",
                    mathematical_expression="a = dv/dt",
                    reasoning="Definition of acceleration",
                    from_equation="F = m(dv/dt)",
                    to_equation="F = ma"
                )
            ],
            validity_conditions=[
                "Constant mass objects",
                "Non-relativistic speeds (v << c)",
                "Inertial reference frames"
            ],
            limitations=[
                "Fails for relativistic speeds",
                "Fails for variable mass systems",
                "Not valid in accelerating reference frames without fictitious forces"
            ]
        )
        assert derivation.equation == "F = ma"
        assert len(derivation.derivation_steps) == 5
        assert derivation.derivation_steps[4].to_equation == "F = ma"
