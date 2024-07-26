#!/bin/sh

# Start FastAPI
uvicorn Rag_app.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit
streamlit run Rag_app/frontend/streamlit.py
