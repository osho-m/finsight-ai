from pydantic import BaseModel, Field


class Company(BaseModel):
    ticker: str
    name: str
    sector: str
    description: str


class AnalysisRequest(BaseModel):
    ticker: str = Field(..., examples=["NOVA"])
    question: str = Field(
        default="What are the main upside and downside risks?",
        examples=["Should this company be considered for a medium-risk growth portfolio?"],
    )


class AgentScores(BaseModel):
    research: int
    news: int
    quant: int
    rag: int


class AnalysisResponse(BaseModel):
    ticker: str
    signal: str
    confidence: int
    composite_score: int
    agent_scores: AgentScores
    executive_summary: str
    grounded_answer: str
    reasoning: list[str]
    risk_flags: list[str]


class CompanyListResponse(BaseModel):
    companies: list[Company]
