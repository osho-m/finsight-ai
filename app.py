import streamlit as st
import plotly.graph_objects as go

from finsight.agents import run_investment_committee
from finsight.quant import get_price_frame
from finsight.store import get_company, list_companies


st.set_page_config(
    page_title="FinSight AI",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)


def signal_color(signal: str) -> str:
    return {"BUY": "#15803d", "HOLD": "#a16207", "SELL": "#b91c1c"}.get(signal, "#334155")


def price_chart(ticker: str) -> go.Figure:
    prices = get_price_frame(ticker)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=prices["day"],
            y=prices["close"],
            mode="lines",
            name="Close",
            line={"color": "#2563eb", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=prices["day"],
            y=prices["sma_20"],
            mode="lines",
            name="SMA 20",
            line={"color": "#f97316", "width": 1.5},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=prices["day"],
            y=prices["sma_50"],
            mode="lines",
            name="SMA 50",
            line={"color": "#64748b", "width": 1.5},
        )
    )
    fig.update_layout(
        height=360,
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        legend={"orientation": "h", "y": 1.05},
        xaxis_title="Trading Day",
        yaxis_title="Synthetic Price",
    )
    return fig


st.title("FinSight AI")
st.caption("Multi-agent financial intelligence system for explainable investment research.")

companies = list_companies()
tickers = [company.ticker for company in companies]

with st.sidebar:
    st.header("Analysis")
    ticker = st.selectbox("Company", tickers, index=0)
    question = st.text_area(
        "Research question",
        value="What are the main upside and downside risks for this company?",
        height=120,
    )
    run_button = st.button("Run Agent Committee", type="primary", use_container_width=True)

company = get_company(ticker)

if run_button or "last_result" not in st.session_state or st.session_state.get("last_ticker") != ticker:
    st.session_state["last_result"] = run_investment_committee(ticker, question)
    st.session_state["last_ticker"] = ticker

result = st.session_state["last_result"]

left, right = st.columns([1, 2])

with left:
    st.subheader(f"{company.name} ({company.ticker})")
    st.write(company.description)
    st.metric("Final Signal", result.signal)
    st.metric("Confidence", f"{result.confidence}%")
    st.metric("Composite Score", f"{result.composite_score}/100")
    st.markdown(
        f"<div style='height:8px;background:{signal_color(result.signal)};border-radius:4px'></div>",
        unsafe_allow_html=True,
    )

with right:
    st.plotly_chart(price_chart(ticker), use_container_width=True)

st.subheader("Agent Committee Output")
cols = st.columns(4)
cols[0].metric("Research", f"{result.agent_scores.research}/100")
cols[1].metric("News", f"{result.agent_scores.news}/100")
cols[2].metric("Quant", f"{result.agent_scores.quant}/100")
cols[3].metric("RAG Confidence", f"{result.agent_scores.rag}/100")

st.write(result.executive_summary)

tab1, tab2, tab3, tab4 = st.tabs(["Reasoning", "Risk Flags", "Grounded Answer", "API Payload"])

with tab1:
    for item in result.reasoning:
        st.markdown(f"- {item}")

with tab2:
    if result.risk_flags:
        for risk in result.risk_flags:
            st.warning(risk)
    else:
        st.success("No severe risk flags detected by the committee.")

with tab3:
    st.markdown(result.grounded_answer)
    st.caption("Answer generated from retrieved company filing snippets in the local knowledge base.")

with tab4:
    st.json(result.model_dump())

st.caption("Educational portfolio project only. Not financial advice.")
