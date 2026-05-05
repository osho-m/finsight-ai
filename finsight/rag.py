import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from finsight.store import get_filings


def retrieve_context(ticker: str, question: str, top_k: int = 2) -> list[str]:
    documents = get_filings(ticker)
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(documents + [question])
    similarities = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    ranked = similarities.argsort()[::-1][:top_k]
    return [documents[index] for index in ranked]


def rag_agent(ticker: str, question: str) -> dict:
    context = retrieve_context(ticker, question)
    joined = " ".join(context)
    confidence = 70 + min(len(context) * 8, 20)
    answer = generate_grounded_answer(question, context, joined)
    return {"score": min(confidence, 95), "answer": answer, "sources": context}


def generate_grounded_answer(question: str, context: list[str], joined_context: str) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return (
            f"Question: {question}\n\n"
            f"Grounded answer: Based on retrieved filing context, {joined_context} "
            "The agent recommends treating the signal as explainable research support, not a standalone investment decision."
        )

    try:
        from openai import OpenAI

        client = OpenAI()
        response = client.chat.completions.create(
            model=os.getenv("FINSIGHT_LLM_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a financial research assistant. Answer only from the provided context. "
                        "Be concise, cite the relevant evidence, and do not provide financial advice."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Question: {question}\n\nContext:\n" + "\n".join(f"- {item}" for item in context),
                },
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content or joined_context
    except Exception:
        return (
            f"Question: {question}\n\n"
            f"Grounded answer: Based on retrieved filing context, {joined_context} "
            "The hosted fallback stayed deterministic because the LLM call was unavailable."
        )
