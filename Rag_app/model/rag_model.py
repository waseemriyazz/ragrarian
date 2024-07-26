from openai import OpenAI
from Rag_app.config.config import OPENAI_API_BASE_URL, OPENAI_API_KEY, MODEL_NAME, EMBEDDING_MODEL
from Rag_app.core.utils import get_vector_stores, SimpleDocument
from sentence_transformers import SentenceTransformer
import numpy as np

class RAGModel:
    def __init__(self):
        self.client = OpenAI(base_url=OPENAI_API_BASE_URL, api_key=OPENAI_API_KEY)
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    def handle_query(self, query):
        # Get all vector stores
        vector_stores = get_vector_stores()
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0]
        
        # Search across all vector stores
        results = []
        for store in vector_stores:
            distances, indices = store.index.search(np.array([query_embedding]), k=5)
            for i, idx in enumerate(indices[0]):
                doc = SimpleDocument(store.docstore[idx], {"score": float(distances[0][i])})
                results.append(doc)
        
        # Sort results by relevance score
        results.sort(key=lambda x: x.metadata['score'])
        
        # Take top 5 results
        top_results = results[:5]
        
        # Prepare context with relevance scores
        context = "\n\n".join([f"Relevance: {doc.metadata['score']:.4f}\nContent: {doc.page_content}" for doc in top_results])

        # Prepare the prompt for the language model
        system_message = """You are a helpful AI assistant. Your task is to answer the user's query based on the provided context. 
        Follow these guidelines:
        1. Use only the information from the given context to answer the query.
        2. If the context doesn't contain relevant information, say "I don't have enough information to answer that question."
        3. Cite the relevance scores when referring to specific pieces of information.
        4. Provide a concise yet informative answer."""

        # Generate response using OpenAI
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Context:\n{context}\n\nQuery: {query}"}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content

    def rephrase_text(self, text, format_option):
        if format_option == 'Bullet Points':
            rephrase_prompt = f"Rephrase the following text in bullet points:\n{text}"
        elif format_option == 'Paragraph':
            rephrase_prompt = f"Rephrase the following text as a paragraph:\n{text}"
        elif format_option == 'Concise':
            rephrase_prompt = f"Rephrase the following text concisely:\n{text}"
        elif format_option == 'Detailed':
            rephrase_prompt = f"Rephrase the following text in detail:\n{text}"
        else:
            rephrase_prompt = f"Rephrase the following text:\n{text}"

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a rephrasing assistant."},
                {"role": "user", "content": rephrase_prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        return response.choices[0].message.content