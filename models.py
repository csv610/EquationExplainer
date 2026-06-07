from pydantic import BaseModel, Field


class SourceCitation(BaseModel):
    model_config = {"extra": "forbid"}
    title: str = Field(..., description="Title of the publication or work")
    authors: str = Field(..., description="Author(s) of the publication")
    year: int = Field(..., description="Year of publication")
    journal: str = Field(..., description="Journal, proceedings, or book where published")
    url: str | None = Field(None, description="URL if publicly available")


class IntroductionModel(BaseModel):
    model_config = {"extra": "forbid"}
    equation_name: str = Field(..., description="Name of the equation")
    equation: str = Field(..., description="The equation in LaTeX or plain text format")
    overview: str = Field(..., description="Brief overview of what the equation describes")
    significance: str = Field(..., description="Why this equation is important in physics")
    context: str = Field(..., description="The field of physics and broader context")
    key_variables: dict[str, str] = Field(
        default_factory=dict, description="Dictionary mapping variable names to their meanings"
    )


class EquationExplanation(BaseModel):
    model_config = {"extra": "forbid"}
    simple_explanation: str = Field(..., description="Simple explanation for beginners")
    detailed_explanation: str = Field(..., description="Detailed explanation with more depth")
    real_world_example: str = Field(..., description="Real-world example of this equation in action")
    key_concepts: list[str] = Field(..., description="List of key concepts related to this equation")
    introduction: IntroductionModel | None = Field(None, description="Introduction to the equation")


class ApplicationModel(BaseModel):
    model_config = {"extra": "forbid"}
    title: str = Field(..., description="Title of the application")
    description: str = Field(..., description="Description of how the equation is applied")


class HistoryModel(BaseModel):
    model_config = {"extra": "forbid"}
    year_discovered: int = Field(..., description="Year the equation was discovered or developed")
    discoverer: str = Field(..., description="Scientist(s) who discovered/developed the equation")
    historical_context: str = Field(..., description="Historical and scientific context of the discovery")
    earlier_related_equations: list[str] | None = Field(
        default=None, description="Earlier equations or concepts that led to this equation"
    )
    key_developments: list[str] | None = Field(
        default=None, description="Timeline of key developments and refinements"
    )
    impact: str = Field(..., description="Impact on physics and science")
    source_citations: list[SourceCitation] = Field(
        default_factory=list,
        description="Published sources supporting the historical claims made about this equation",
    )
    original_publication: str | None = Field(
        None, description="Original publication details (journal, paper title, etc.)"
    )
    country_of_origin: str | None = Field(None, description="Country where the equation was developed")
    competing_theories: list[str] | None = Field(
        default=None, description="Competing theories or equations from the same period"
    )
    applications: list[ApplicationModel] | None = Field(
        default=None, description="Modern applications and use cases of the equation"
    )


class DerivationStep(BaseModel):
    model_config = {"extra": "forbid"}
    step_number: int = Field(..., description="Sequential step number")
    title: str = Field(..., description="Title or name of this step")
    description: str = Field(..., description="Detailed description of what happens in this step")
    mathematical_expression: str = Field(..., description="Mathematical expression or operation in this step")
    reasoning: str = Field(..., description="Reasoning for this step")
    from_equation: str | None = Field(None, description="Starting equation or expression for this step")
    to_equation: str | None = Field(None, description="Resulting equation or expression after this step")


class DerivationModel(BaseModel):
    model_config = {"extra": "forbid"}
    starting_principles: list[str] = Field(
        ..., description="Fundamental principles, laws, or axioms used as starting points"
    )
    derivation_steps: list[DerivationStep] = Field(..., description="Step-by-step derivation process")
    alternative_derivations: list[str] | None = Field(
        default=None, description="Alternative methods or paths to derive the same equation"
    )
    special_cases: list[str] | None = Field(
        default=None, description="Special cases or simplified versions of the equation"
    )
    validity_conditions: list[str] | None = Field(
        default=None, description="Conditions under which the equation is valid"
    )
    limitations: list[str] | None = Field(default=None, description="Limitations or constraints of the equation")
    extensions_generalizations: list[str] | None = Field(
        default=None, description="Ways the equation has been extended or generalized"
    )
    mathematical_prerequisites: list[str] | None = Field(
        default=None, description="Mathematical knowledge required to understand the derivation"
    )
    related_equations: list[str] | None = Field(
        default=None, description="Related equations or formulas derived from this equation"
    )


class EquationModel(BaseModel):
    model_config = {"extra": "forbid"}
    name: str = Field(..., description="Name of the equation")
    equation: str = Field(..., description="The equation in LaTeX or plain text format")
    context: str | None = Field(None, description="Context or area of physics where this applies")
    difficulty: str | None = Field(None, description="Difficulty level: beginner, intermediate, or advanced")
