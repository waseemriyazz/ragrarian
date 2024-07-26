#!/bin/bash

# Start FastAPI
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit
poetry run streamlit run frontend/streamlit.py