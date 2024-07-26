import streamlit as st
import requests

# API URL
API_URL = "http://localhost:8000"

# Apply custom CSS for improved styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
        padding: 20px;
        font-family: Arial, sans-serif;
    }
    .stButton > button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    .stTextInput > div > input {
        background-color: #ffffff;
        border: 1px solid #ced4da;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    .stTextArea > div > textarea {
        border-radius: 5px;
        font-size: 16px;
    }
    .stFileUploader {
        border: 2px dashed #007bff;
        padding: 10px;
        border-radius: 5px;
    }
    .stSpinner {
        color: #007bff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header and Caption
st.title("Chat with PDF")
st.subheader("Developed by the Baingan Team")

# Initialize session state
if "answer" not in st.session_state:
    st.session_state.answer = ""

if "rephrased_answer" not in st.session_state:
    st.session_state.rephrased_answer = ""

# Upload PDF files
st.subheader("Upload PDF Files")
pdf_files = st.file_uploader("Choose PDF files", type='pdf', accept_multiple_files=True, label_visibility="collapsed")

if pdf_files:
    for pdf in pdf_files:
        with st.spinner(f"Processing {pdf.name}..."):
            files = {"file": pdf.getvalue()}
            response = requests.post(f"{API_URL}/upload_pdf", files=files)
            if response.status_code == 200:
                st.success(f"PDF '{pdf.name}' processed successfully")
            else:
                st.error(f"Error processing PDF '{pdf.name}'")

# Manage vector database
st.subheader("Manage Vector Databases")
if st.button("Delete Vector Database"):
    with st.spinner("Deleting vector database..."):
        response = requests.post(f"{API_URL}/delete_vector_databases")
        if response.status_code == 200:
            st.success("Vector databases deleted successfully")
        else:
            st.error("Error deleting vector databases")

# Query input
st.subheader("Submit Your Query")
query = st.text_input("Enter your query:")

if st.button("Get Answer") and query:
    with st.spinner("Fetching answer..."):
        response = requests.post(f"{API_URL}/query", json={"text": query})
        if response.status_code == 200:
            st.session_state.answer = response.json()["text"]
            st.session_state.rephrased_answer = ""
            st.write("**Answer:**")
            st.write(st.session_state.answer)
        else:
            st.error("Error getting answer")

# Rephrase answer
if st.session_state.answer:
    st.subheader("Rephrase the Answer")
    format_option = st.selectbox(
        "Choose rephrase format:",
        ["Bullet Points", "Paragraph", "Concise", "Detailed"]
    )

    if st.button("Rephrase"):
        with st.spinner("Rephrasing answer..."):
            response = requests.post(f"{API_URL}/rephrase", json={"text": st.session_state.answer, "format_option": format_option})
            if response.status_code == 200:
                st.session_state.rephrased_answer = response.json()["text"]
                st.write("**Original Answer:**")
                st.write(st.session_state.answer)
                st.write("**Rephrased Answer:**")
                st.write(st.session_state.rephrased_answer)
            else:
                st.error("Error rephrasing answer")
