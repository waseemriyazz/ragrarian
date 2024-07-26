import os

OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "http://184.72.115.138:8000/v1/vllm")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "NOT A REAL KEY")
MODEL_NAME = "TechxGenus/Meta-Llama-3-8B-Instruct-AWQ"
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'