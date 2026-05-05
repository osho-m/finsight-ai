from functools import lru_cache

import pandas as pd

from finsight.schemas import Company


COMPANIES = [
    {
        "ticker": "NOVA",
        "name": "NovaGrid Systems",
        "sector": "Clean Energy Infrastructure",
        "description": "Builds grid-scale battery systems, optimization software, and renewable energy storage infrastructure.",
        "revenue_growth": 31.4,
        "gross_margin": 42.0,
        "eps_growth": 18.8,
        "debt_to_equity": 0.41,
        "free_cash_flow_margin": 11.7,
    },
    {
        "ticker": "AURA",
        "name": "Aura Health Analytics",
        "sector": "Healthcare AI",
        "description": "Provides AI-assisted clinical workflow automation, patient risk scoring, and hospital operations analytics.",
        "revenue_growth": 24.1,
        "gross_margin": 55.5,
        "eps_growth": 12.0,
        "debt_to_equity": 0.28,
        "free_cash_flow_margin": 9.8,
    },
    {
        "ticker": "ORBT",
        "name": "OrbitPay Technologies",
        "sector": "Fintech",
        "description": "Operates payment orchestration, fraud analytics, credit risk infrastructure, and merchant finance products.",
        "revenue_growth": 15.7,
        "gross_margin": 38.2,
        "eps_growth": 8.6,
        "debt_to_equity": 0.76,
        "free_cash_flow_margin": 6.1,
    },
    {
        "ticker": "KRYN",
        "name": "Kryon Robotics",
        "sector": "Industrial Automation",
        "description": "Manufactures warehouse robotics, computer vision quality systems, and autonomous factory equipment.",
        "revenue_growth": 19.5,
        "gross_margin": 33.4,
        "eps_growth": -3.1,
        "debt_to_equity": 1.18,
        "free_cash_flow_margin": -2.7,
    },
]


NEWS = {
    "NOVA": [
        "NovaGrid signs multi-year storage contract with European utility",
        "Analysts raise concern about lithium input cost volatility",
        "Company announces strong backlog conversion for grid batteries",
        "New software platform improves battery dispatch efficiency",
    ],
    "AURA": [
        "Aura Health wins hospital AI automation contract",
        "Regulators request additional documentation on clinical workflow model",
        "Customer retention improves after deployment of patient risk suite",
        "Healthcare AI spending remains resilient despite budget pressure",
    ],
    "ORBT": [
        "OrbitPay expands fraud analytics product to Southeast Asia",
        "Merchant lending losses tick higher in latest quarter",
        "Payment volume growth slows as consumer demand moderates",
        "New bank partnership improves settlement reliability",
    ],
    "KRYN": [
        "Kryon Robotics delays shipment of next-generation warehouse robot",
        "Large retailer signs pilot agreement for autonomous picking system",
        "Component shortage weighs on quarterly production",
        "Management reiterates long-term automation demand outlook",
    ],
}


FILINGS = {
    "NOVA": [
        "Management expects demand for grid-scale storage to grow as renewable penetration increases. Backlog quality improved due to longer-duration contracts.",
        "Primary risks include lithium price volatility, project permitting delays, and customer concentration among utility buyers.",
        "The company invested in battery dispatch optimization software to improve recurring revenue and reduce hardware-only margin pressure.",
    ],
    "AURA": [
        "Aura Health Analytics sells AI workflow tools to hospital systems and aims to reduce administrative burden through automation.",
        "Revenue visibility improved with multi-year SaaS contracts, but regulatory review and model validation requirements can lengthen sales cycles.",
        "Management highlighted patient risk scoring, clinical documentation support, and hospital capacity forecasting as key growth areas.",
    ],
    "ORBT": [
        "OrbitPay processes merchant transactions and provides fraud analytics, settlement routing, and embedded credit products.",
        "Credit exposure from merchant financing may increase losses during weak macroeconomic periods.",
        "The company is investing in real-time fraud detection and payment reliability to protect enterprise merchant retention.",
    ],
    "KRYN": [
        "Kryon Robotics sells automation hardware and software to warehouses, factories, and logistics operators.",
        "Gross margin remains pressured by component costs, delayed shipments, and implementation complexity.",
        "Management believes labor shortages support long-term robotics demand, but near-term execution risk remains elevated.",
    ],
}


@lru_cache(maxsize=1)
def fundamentals_frame() -> pd.DataFrame:
    return pd.DataFrame(COMPANIES)


def list_companies() -> list[Company]:
    return [
        Company(
            ticker=item["ticker"],
            name=item["name"],
            sector=item["sector"],
            description=item["description"],
        )
        for item in COMPANIES
    ]


def get_company(ticker: str) -> Company:
    ticker = ticker.upper()
    row = fundamentals_frame().query("ticker == @ticker")
    if row.empty:
        raise ValueError(f"Unknown ticker: {ticker}")
    item = row.iloc[0].to_dict()
    return Company(
        ticker=item["ticker"],
        name=item["name"],
        sector=item["sector"],
        description=item["description"],
    )


def get_fundamentals(ticker: str) -> dict:
    ticker = ticker.upper()
    row = fundamentals_frame().query("ticker == @ticker")
    if row.empty:
        raise ValueError(f"Unknown ticker: {ticker}")
    return row.iloc[0].to_dict()


def get_news(ticker: str) -> list[str]:
    return NEWS[ticker.upper()]


def get_filings(ticker: str) -> list[str]:
    return FILINGS[ticker.upper()]
