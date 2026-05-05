from finsight.quant import quant_agent
from finsight.rag import rag_agent
from finsight.schemas import AgentScores, AnalysisResponse
from finsight.store import get_company, get_fundamentals, get_news


POSITIVE_TERMS = {
    "wins",
    "improves",
    "strong",
    "growth",
    "raises",
    "expands",
    "partnership",
    "contract",
    "resilient",
    "conversion",
}

NEGATIVE_TERMS = {
    "concern",
    "volatility",
    "losses",
    "slows",
    "delays",
    "shortage",
    "pressure",
    "regulators",
    "risk",
}


def research_agent(ticker: str) -> dict:
    item = get_fundamentals(ticker)
    score = 50
    score += min(max(item["revenue_growth"], -10), 35) * 0.7
    score += min(max(item["gross_margin"] - 30, -10), 30) * 0.5
    score += min(max(item["eps_growth"], -20), 25) * 0.5
    score += min(max(item["free_cash_flow_margin"], -15), 20) * 0.8
    score -= min(max(item["debt_to_equity"] - 0.4, 0), 1.5) * 18
    score = int(round(min(max(score, 0), 100)))

    strengths = []
    risks = []
    if item["revenue_growth"] >= 20:
        strengths.append("high revenue growth")
    if item["gross_margin"] >= 45:
        strengths.append("premium margin profile")
    if item["free_cash_flow_margin"] >= 8:
        strengths.append("healthy free-cash-flow margin")
    if item["debt_to_equity"] >= 1:
        risks.append("elevated leverage")
    if item["free_cash_flow_margin"] < 0:
        risks.append("negative free cash flow")
    if item["eps_growth"] < 0:
        risks.append("declining EPS trend")

    return {"score": score, "strengths": strengths, "risks": risks}


def news_agent(ticker: str) -> dict:
    headlines = get_news(ticker)
    total = 0
    observations = []
    for headline in headlines:
        words = set(headline.lower().replace("-", " ").split())
        positive_hits = len(words & POSITIVE_TERMS)
        negative_hits = len(words & NEGATIVE_TERMS)
        total += positive_hits - negative_hits
        if positive_hits or negative_hits:
            observations.append(headline)

    score = int(round(min(max(55 + total * 8, 0), 100)))
    return {"score": score, "headlines": headlines, "observations": observations}


def decide_signal(score: int) -> str:
    if score >= 72:
        return "BUY"
    if score >= 48:
        return "HOLD"
    return "SELL"


def build_risk_flags(research: dict, quant: dict, news: dict) -> list[str]:
    flags = []
    flags.extend(research["risks"])
    if quant["volatility"] >= 35:
        flags.append("high realized volatility")
    if quant["max_drawdown"] <= -25:
        flags.append("material recent drawdown")
    if news["score"] < 50:
        flags.append("negative news sentiment")
    return flags


def run_investment_committee(ticker: str, question: str) -> AnalysisResponse:
    ticker = ticker.upper()
    company = get_company(ticker)
    research = research_agent(ticker)
    news = news_agent(ticker)
    quant = quant_agent(ticker)
    rag = rag_agent(ticker, question)

    composite = int(
        round(
            research["score"] * 0.35
            + news["score"] * 0.20
            + quant["score"] * 0.30
            + rag["score"] * 0.15
        )
    )
    signal = decide_signal(composite)
    confidence = int(round(62 + abs(composite - 50) * 0.55))
    confidence = min(max(confidence, 55), 92)
    risks = build_risk_flags(research, quant, news)

    reasoning = [
        f"Research Agent scored {research['score']}/100 based on fundamentals for {company.name}.",
        f"News Agent scored {news['score']}/100 after reading {len(news['headlines'])} recent headlines.",
        f"Quant Agent scored {quant['score']}/100 with {quant['momentum']}% momentum, {quant['volatility']}% volatility, and RSI {quant['rsi']}.",
        f"RAG Agent scored {rag['score']}/100 using filing-style context retrieved for the research question.",
    ]

    if research["strengths"]:
        reasoning.append("Key fundamental strengths: " + ", ".join(research["strengths"]) + ".")
    if risks:
        reasoning.append("The committee reduced conviction due to: " + ", ".join(risks) + ".")

    summary = (
        f"The agent committee rates {company.name} as {signal} with {confidence}% confidence. "
        f"The composite score is {composite}/100, balancing fundamentals, sentiment, technical behavior, and filing-grounded context."
    )

    return AnalysisResponse(
        ticker=ticker,
        signal=signal,
        confidence=confidence,
        composite_score=composite,
        agent_scores=AgentScores(
            research=research["score"],
            news=news["score"],
            quant=quant["score"],
            rag=rag["score"],
        ),
        executive_summary=summary,
        grounded_answer=rag["answer"],
        reasoning=reasoning,
        risk_flags=risks,
    )
