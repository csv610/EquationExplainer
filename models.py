from pydantic import BaseModel, Field
from typing import Optional


class PhysicsEquation(BaseModel):
    """Model for a physics equation"""

    name: str = Field(..., description="Name of the equation (e.g., 'Newton's Second Law')")
    equation: str = Field(..., description="The equation in LaTeX or plain text format")
    context: Optional[str] = Field(None, description="Context or area of physics where this applies")
    variables: Optional[dict[str, str]] = Field(
        default=None, description="Dictionary mapping variable names to their meanings"
    )


class IntroductionModel(BaseModel):
    """Model for the introduction to a physics equation"""

    equation_name: str = Field(..., description="Name of the equation")
    equation: str = Field(..., description="The equation in LaTeX or plain text format")
    overview: str = Field(..., description="Brief overview of what the equation describes")
    significance: str = Field(..., description="Why this equation is important in physics")
    context: str = Field(..., description="The field of physics and broader context")
    key_variables: dict[str, str] = Field(
        default_factory=dict, description="Dictionary mapping variable names to their meanings"
    )


class EquationExplanation(BaseModel):
    """Model for the explanation of a physics equation"""

    equation_name: str = Field(..., description="Name of the equation being explained")
    equation: str = Field(..., description="The equation itself")
    simple_explanation: str = Field(..., description="Simple explanation for beginners")
    detailed_explanation: str = Field(..., description="Detailed explanation with more depth")
    real_world_example: str = Field(..., description="Real-world example of this equation in action")
    key_concepts: list[str] = Field(..., description="List of key concepts related to this equation")
    introduction: Optional[IntroductionModel] = Field(None, description="Introduction to the equation")


class ExplanationRequest(BaseModel):
    """Model for requesting an equation explanation"""

    equation: str = Field(..., description="The physics equation to explain")
    equation_name: Optional[str] = Field(None, description="Name of the equation")
    context: Optional[str] = Field(None, description="Additional context about the equation")
    difficulty_level: str = Field(
        default="intermediate", description="Difficulty level: 'beginner', 'intermediate', or 'advanced'"
    )


class ApplicationModel(BaseModel):
    """Model for modern applications of an equation"""

    title: str = Field(..., description="Title of the application")
    description: str = Field(..., description="Description of how the equation is applied")


class HistoryModel(BaseModel):
    """Model for the historical development of a physics equation"""

    equation_name: str = Field(..., description="Name of the equation")
    equation: str = Field(..., description="The equation in LaTeX or plain text format")
    year_discovered: int = Field(..., description="Year the equation was discovered or developed")
    discoverer: str = Field(..., description="Scientist(s) who discovered/developed the equation")
    historical_context: str = Field(..., description="Historical and scientific context of the discovery")
    earlier_related_equations: Optional[list[str]] = Field(
        default=None, description="Earlier equations or concepts that led to this equation"
    )
    key_developments: Optional[list[str]] = Field(
        default=None, description="Timeline of key developments and refinements"
    )
    impact: str = Field(..., description="Impact on physics and science")
    original_publication: Optional[str] = Field(
        None, description="Original publication details (journal, paper title, etc.)"
    )
    country_of_origin: Optional[str] = Field(None, description="Country where the equation was developed")
    competing_theories: Optional[list[str]] = Field(
        default=None, description="Competing theories or equations from the same period"
    )
    applications: Optional[list[ApplicationModel]] = Field(
        default=None, description="Modern applications and use cases of the equation"
    )


class DerivationStep(BaseModel):
    """Model for a single step in equation derivation"""

    step_number: int = Field(..., description="Sequential step number")
    title: str = Field(..., description="Title or name of this step")
    description: str = Field(..., description="Detailed description of what happens in this step")
    mathematical_expression: str = Field(..., description="Mathematical expression or operation in this step")
    reasoning: str = Field(..., description="Reasoning or justification for this step")
    from_equation: Optional[str] = Field(None, description="Starting equation or expression for this step")
    to_equation: Optional[str] = Field(None, description="Resulting equation or expression after this step")


class DerivationModel(BaseModel):
    """Model for the derivation of a physics equation"""

    equation_name: str = Field(..., description="Name of the equation")
    equation: str = Field(..., description="The final derived equation")
    starting_principles: list[str] = Field(
        ..., description="Fundamental principles, laws, or axioms used as starting points"
    )
    derivation_steps: list[DerivationStep] = Field(..., description="Step-by-step derivation process")
    alternative_derivations: Optional[list[str]] = Field(
        default=None, description="Alternative methods or paths to derive the same equation"
    )
    special_cases: Optional[list[str]] = Field(
        default=None, description="Special cases or simplified versions of the equation"
    )
    validity_conditions: Optional[list[str]] = Field(
        default=None, description="Conditions under which the equation is valid"
    )
    limitations: Optional[list[str]] = Field(default=None, description="Limitations or constraints of the equation")
    extensions_generalizations: Optional[list[str]] = Field(
        default=None, description="Ways the equation has been extended or generalized"
    )
    mathematical_prerequisites: Optional[list[str]] = Field(
        default=None, description="Mathematical knowledge required to understand the derivation"
    )
    related_equations: Optional[list[str]] = Field(
        default=None, description="Related equations or formulas derived from this equation"
    )


class EquationModel(BaseModel):
    """Comprehensive model for a physics equation with all its aspects"""

    name: str = Field(..., description="Name of the equation")
    equation: str = Field(..., description="The equation in LaTeX or plain text format")
    history: Optional[HistoryModel] = Field(None, description="Historical development of the equation")
    derivation: Optional[DerivationModel] = Field(None, description="Mathematical derivation of the equation")
    applications: Optional[list[ApplicationModel]] = Field(
        default=None, description="Modern applications of the equation"
    )
