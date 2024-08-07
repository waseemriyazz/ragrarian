import streamlit as st
import requests

# API URL
API_URL = "http://localhost:8000"

# Apply custom CSS for a modern AI assistant interface
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f7f9;
        padding: 20px;
        font-family: 'Arial', sans-serif;
    }
    .stButton > button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #0056b3;
        transform: scale(1.05);
    }
    .stTextInput > div > input {
        background-color: #ffffff;
        border: 1px solid #dedede;
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stTextArea > div > textarea {
        border-radius: 10px;
        font-size: 16px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stFileUploader {
        border: 2px dashed #007bff;
        padding: 15px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stSpinner {
        color: #007bff;
    }
    .expander-header {
        background-color: #007bff;
        color: white;
        font-weight: bold;
        font-size: 18px;
        padding: 10px;
        border-radius: 10px;
    }
    .expander-content {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
    }
    .stSlider > div {
        margin-top: 10px;
    }
    .stSelectbox > div {
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header and Caption
st.title("AI Assistant - PDF Interaction")
st.subheader("Powered by the Baingan Team")

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
with st.expander("Manage Vector Databases", expanded=True):
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

# Temperature slider
temperature = st.slider(
    "Select Creativity Level (Temperature)",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    format="%0.1f"
)

if st.button("Get Answer") and query:
    with st.spinner("Fetching answer..."):
        response = requests.post(f"{API_URL}/query", json={"text": query, "temperature": temperature})
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
    with st.expander("Rephrase Options", expanded=True):
        format_option = st.selectbox(
            "Choose rephrase format:",
            ["Bullet Points", "Paragraph", "Concise", "Detailed"]
        )

        if st.button("Rephrase"):
            with st.spinner("Rephrasing answer..."):
                response = requests.post(f"{API_URL}/rephrase", json={"text": st.session_state.answer, "format_option": format_option, "temperature": temperature})
                if response.status_code == 200:
                    st.session_state.rephrased_answer = response.json()["text"]
                    st.write("**Original Answer:**")
                    st.write(st.session_state.answer)
                    st.write("**Rephrased Answer:**")
                    st.write(st.session_state.rephrased_answer)
                else:
                    st.error("Error rephrasing answer")
