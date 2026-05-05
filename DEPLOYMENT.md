# Deployment Guide

## Streamlit Community Cloud

1. Push this repo to GitHub.
2. Create a Streamlit app from the repo.
3. Set `app.py` as the entry file.
4. Add `OPENAI_API_KEY` only if you want generated RAG responses.

## Hugging Face Spaces

1. Create a new Space.
2. Choose Streamlit.
3. Upload the full repo.
4. The app will run from `app.py`.

## FastAPI Backend

For Render or Railway, use:

```bash
uvicorn api:app --host 0.0.0.0 --port $PORT
```

Health check:

```text
GET /
```

Main endpoint:

```text
POST /analyze
```
