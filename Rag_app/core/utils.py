import os
import pickle
import time
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from openai import OpenAI

class SimpleDocument:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata if metadata else {}

def process_pdf(pdf_path):
    start_time = time.time()

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text=text)

    store_name = os.path.splitext(os.path.basename(pdf_path))[0]
    print(f'PDF File: {store_name}')

    model = SentenceTransformer('all-MiniLM-L6-v2')

    vector_store_path = f"data/{store_name}.pkl"
    if os.path.exists(vector_store_path):
        with open(vector_store_path, "rb") as f:
            VectorStore = pickle.load(f)
        print('Embeddings Loaded from the Disk 🍆')
    else:
        embeddings = model.encode(chunks, show_progress_bar=True)
        embeddings = np.array(embeddings)

        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        VectorStore = FAISS(embedding_function=None, docstore=None, index=index, index_to_docstore_id=None)
        VectorStore.docstore = {i: chunk for i, chunk in enumerate(chunks)}
        VectorStore.index_to_docstore_id = {i: i for i in range(len(chunks))}

        with open(vector_store_path, "wb") as f:
            pickle.dump(VectorStore, f)
        print('Embeddings generated and saved to disk 🍆')

    end_time = time.time()
    print(f"Processing time for {store_name}: {end_time - start_time:.2f} seconds")

def handle_query(query):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    k = 5
    results = []
    
    for store_name in os.listdir('data'):
        if store_name.endswith('.pkl'):
            with open(f"data/{store_name}", "rb") as f:
                VectorStore = pickle.load(f)
            query_embedding = model.encode([query])
            distances, indices = VectorStore.index.search(query_embedding, k)
            docs = [SimpleDocument(VectorStore.docstore[idx], {"score": float(distances[0][i])}) for i, idx in enumerate(indices[0])]
            results.extend(docs)
    results.sort(key=lambda x: x.metadata['score'])
    top_results = results[:k]
    context = "\n\n".join([f"Relevance: {doc.metadata['score']:.4f}\nContent: {doc.page_content}" for doc in top_results])
    client = OpenAI(
        base_url="http://184.72.115.138:8000/v1/vllm",
        api_key="NOT A REAL KEY",
    )
    system_message = """You are a helpful AI assistant. Your task is to answer the user's query based on the provided context. 
    Follow these guidelines:
    1. Use only the information from the given context to answer the query.
    2. If the context doesn't contain relevant information, say "I don't have enough information to answer that question."
    3. Cite the relevance scores when referring to specific pieces of information.
    4. Provide a concise yet informative answer."""
    response = client.chat.completions.create(
        model="TechxGenus/Meta-Llama-3-8B-Instruct-AWQ",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Context:\n{context}\n\nQuery: {query}"}
        ],
        max_tokens=300,
        temperature=1
    )
    answer = response.choices[0].message.content
    return answer
def rephrase_text(text, format_option):
    client = OpenAI(
        base_url="http://184.72.115.138:8000/v1/vllm",
        api_key="NOT A REAL KEY",
    )
    if format_option == 'Bullet Points':
        rephrase_prompt = f"Rephrase the following text in bullet points:\n{text}"
    elif format_option == 'Paragraph':
        rephrase_prompt = f"Rephrase the following text as a paragraph:\n{text}"
    elif format_option == 'Concise':
        rephrase_prompt = f"Rephrase the following text concisely:\n{text}"
    elif format_option == 'Detailed':
        rephrase_prompt = f"Rephrase the following text in detail:\n{text}"
    response = client.chat.completions.create(
        model="TechxGenus/Meta-Llama-3-8B-Instruct-AWQ",
        messages=[
            {"role": "system", "content": "You are a rephrasing assistant."},
            {"role": "user", "content": rephrase_prompt}
        ]
    )
    rephrased_text = response.choices[0].message.content
    return rephrased_text