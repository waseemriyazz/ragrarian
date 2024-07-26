import os

OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "http://44.211.211.39:8000/v1/vllm")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "NOT A REAL KEY")
MODEL_NAME = "TechxGenus/Meta-Llama-3-8B-Instruct-AWQ"
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'