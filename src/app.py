
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LangChain & Google GenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Local imports
# Ensure we can import from src if running from root
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.ingest import create_vector_db, get_vector_db

# Page Config
st.set_page_config(page_title="DocuSense", page_icon="📚", layout="wide")

st.title("📚 DocuSense: RAG with Google Gemini")

# Sidebar for controls
with st.sidebar:
    st.header("Settings")
    
    # API Key check
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("⚠️ GOOGLE_API_KEY missing in .env")
        st.stop()
    else:
        st.success("API Key loaded")
    
    st.subheader("Document Ingestion")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    if st.button("Process Document"):
        if uploaded_file:
            with st.spinner("Processing PDF..."):
                try:
                    create_vector_db(uploaded_file)
                    st.success("Done! Vector DB created.")
                except Exception as e:
                    st.error(f"Error processing file: {e}")
        else:
            st.warning("Please upload a file first.")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # 1. Load Vector DB
                db = get_vector_db()
                if not db:
                    st.warning("No vector database found. Please upload and process a PDF first.")
                else:
                    # 2. Setup Retriever
                    retriever = db.as_retriever(search_kwargs={"k": 5})
                    
                    # 3. Setup LLM
                    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
                    
                    # 4. Setup Prompt
                    template = """Answer the question based only on the following context:
                    {context}

                    Question: {question}
                    """
                    prompt_template = ChatPromptTemplate.from_template(template)
                    
                    # 5. Build Chain (LCEL)
                    def format_docs(docs):
                        return "\n\n".join([d.page_content for d in docs])

                    chain = (
                        {"context": retriever | format_docs, "question": RunnablePassthrough()}
                        | prompt_template
                        | llm
                        | StrOutputParser()
                    )
                    
                    # 6. Invoke
                    response = chain.invoke(prompt)
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")

