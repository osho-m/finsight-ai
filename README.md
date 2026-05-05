---
title: FinSight AI
emoji: 📈
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
app_port: 8501
pinned: false
---

# FinSight AI

Multi-agent financial intelligence platform that analyzes fundamentals, market behavior, news sentiment, and company filings to generate explainable BUY / HOLD / SELL signals.

This project is designed as a portfolio-grade GenAI engineering project: it has a live Streamlit app, a FastAPI serving layer, retrieval-augmented Q&A, agent orchestration, explainable scoring, reproducible synthetic data, and Kaggle/GitHub-ready documentation.

## Why This Project Stands Out

Most finance AI demos are either a stock-price notebook or a PDF chatbot. FinSight AI combines both product and engineering:

- Multi-agent architecture with specialist agents
- Retrieval-augmented generation over filing-style documents
- Quantitative signal engine with RSI, volatility, momentum, drawdown, and moving-average crossover
- Sentiment analysis over market news
- FastAPI prediction endpoint with typed request/response schemas
- Streamlit dashboard deployable on Hugging Face Spaces
- Synthetic dataset suitable for Kaggle upload

## Agent System

FinSight uses five agents:

1. Research Agent
   Analyzes revenue growth, margin trend, debt, EPS, and cash-flow quality.

2. News Agent
   Scores market headlines and detects sentiment shifts.

3. Quant Agent
   Computes technical indicators and market risk metrics.

4. RAG Agent
   Retrieves grounded context from filing-style company documents.

5. Orchestrator Agent
   Combines agent outputs into a final signal, confidence score, risk flags, and explanation.

## Tech Stack

- Python
- Streamlit
- FastAPI
- Pandas
- NumPy
- Scikit-learn
- FAISS-compatible local vector retrieval using TF-IDF fallback
- Pydantic
- Plotly
- Uvicorn
- Optional OpenAI API integration for generated RAG answers

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open the app at:

```text
http://localhost:8501
```

Optional GenAI mode:

```bash
copy .env.example .env
set OPENAI_API_KEY=your_key_here
```

Without an API key, FinSight still runs using deterministic grounded synthesis so the public demo does not break.

To run the API:

```bash
uvicorn api:app --reload
```

API docs:

```text
http://localhost:8000/docs
```

## Example API Request

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d "{\"ticker\":\"NOVA\",\"question\":\"What are the main upside and downside risks?\"}"
```

## Deploy

### Hugging Face Spaces

Create a new Streamlit Space and upload:

- `app.py`
- `requirements.txt`
- `finsight/`
- `data/`
- `README.md`

The app runs without external keys.

For generated RAG answers, add `OPENAI_API_KEY` as a Space secret.

### Render / Railway API

Use this start command:

```bash
uvicorn api:app --host 0.0.0.0 --port $PORT
```

## Resume Bullets

- Built FinSight AI, a multi-agent financial intelligence platform using Streamlit, FastAPI, RAG, and quantitative signal models to generate explainable BUY / HOLD / SELL recommendations.
- Designed five-agent workflow for fundamentals research, news sentiment, technical indicators, filing retrieval, and final investment-signal orchestration.
- Implemented production-style API serving with typed schemas, confidence scoring, risk flags, and grounded document answers for company analysis.

## LinkedIn Post

I built FinSight AI, a multi-agent financial intelligence platform that simulates how an AI analyst team could evaluate companies.

The system uses five agents:

- Research Agent for fundamentals
- News Agent for sentiment shifts
- Quant Agent for RSI, momentum, volatility, and trend
- RAG Agent for filing-grounded Q&A
- Orchestrator Agent for final BUY / HOLD / SELL signal

Tech stack: Python, Streamlit, FastAPI, Pandas, Scikit-learn, Plotly, RAG, agent orchestration.

What makes it different from a normal stock dashboard: every recommendation is explainable, grounded in retrieved filing context, and served through both a dashboard and an API.

#AI #GenAI #MachineLearning #Python #Finance #RAG #FastAPI #Streamlit

## Disclaimer

This project is for education and portfolio demonstration only. It is not financial advice.
