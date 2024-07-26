import streamlit as st
import requests
import os

API_URL = "http://localhost:8000"

st.header("Chat with PDF 💬")
st.caption("made by Baingan team 🍆")

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "rephrased_answer" not in st.session_state:
    st.session_state.rephrased_answer = ""

# Upload PDF files
pdf_files = st.file_uploader("Upload your PDFs", type='pdf', accept_multiple_files=True)

if pdf_files:
    for pdf in pdf_files:
        files = {"file": pdf.getvalue()}
        response = requests.post(f"{API_URL}/upload_pdf", files=files)
        if response.status_code == 200:
            st.success(f"PDF {pdf.name} processed successfully")
        else:
            st.error(f"Error processing PDF {pdf.name}")

# Button to delete the vector database
if st.button("Delete vector database"):
    response = requests.post(f"{API_URL}/delete_vector_databases")
    if response.status_code == 200:
        st.success(f"Vector databases deleted: {response.json()['message']}")
    else:
        st.error("Error deleting vector databases")

# Query input
query = st.text_input("Enter your query:")

if st.button("Get Answer") and query:
    response = requests.post(f"{API_URL}/query", json={"text": query})
    if response.status_code == 200:
        st.session_state.answer = response.json()["text"]
        st.session_state.rephrased_answer = ""
        st.write("Answer:")
        st.write(st.session_state.answer)
    else:
        st.error("Error getting answer")

if st.session_state.answer:
    format_option = st.selectbox(
        "Choose the rephrase format:",
        ["Bullet Points", "Paragraph", "Concise", "Detailed"]
    )

    if st.button("🔄 Rephrase"):
        response = requests.post(f"{API_URL}/rephrase", json={"text": st.session_state.answer, "format_option": format_option})
        if response.status_code == 200:
            st.session_state.rephrased_answer = response.json()["text"]
            st.write("Original Answer:")
            st.write(st.session_state.answer)
            st.write("Rephrased Answer:")
            st.write(st.session_state.rephrased_answer)
        else:
            st.error("Error rephrasing answer")