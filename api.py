from fastapi import FastAPI

from finsight.agents import run_investment_committee
from finsight.schemas import AnalysisRequest, AnalysisResponse, CompanyListResponse
from finsight.store import list_companies

app = FastAPI(
    title="FinSight AI API",
    description="Multi-agent financial intelligence API for explainable company analysis.",
    version="1.0.0",
)


@app.get("/", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "FinSight AI"}


@app.get("/companies", response_model=CompanyListResponse, tags=["companies"])
def companies() -> CompanyListResponse:
    return CompanyListResponse(companies=list_companies())


@app.post("/analyze", response_model=AnalysisResponse, tags=["analysis"])
def analyze(request: AnalysisRequest) -> AnalysisResponse:
    return run_investment_committee(request.ticker, request.question)
