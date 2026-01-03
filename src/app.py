import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from ingest import create_vector_db, get_vector_db

# Load environment variables (API Key)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
google_api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="ClarifAI: Document Simplifier", page_icon="�", layout="wide")

st.title("� ClarifAI")
st.markdown("""
**Upload any document (Legal, Medical, or General)** and I will explain it in plain English.
""")

# Sidebar for Upload
with st.sidebar:
    st.header("📂 Document Upload")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    if st.button("Analyze Document"):
        if uploaded_file and google_api_key:
            with st.spinner("Processing document... This might take a minute."):
                try:
                    db = create_vector_db(uploaded_file)
                    st.success("Document processed successfully! You can now ask questions.")
                    st.session_state['processed'] = True
                except Exception as e:
                    st.error(f"Error processing document: {e}")
        elif not google_api_key:
            st.error("API Key missing. Please check .env file.")
        else:
            st.warning("Please upload a PDF first.")

# Main Chat Interface
if 'processed' in st.session_state and st.session_state['processed']:
    st.divider()
    user_question = st.text_input("Ask a question about your document:")
    
    if user_question:
        with st.spinner("Thinking..."):
            try:
                # 1. Load Vector DB
                db = get_vector_db()
                if not db:
                    st.error("Database not found. Please upload a file again.")
                    st.stop()
                
                # 2. Setup Retriever
                retriever = db.as_retriever(search_kwargs={"k": 3})
                
                # 3. Setup LLM (Gemini)
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=google_api_key, temperature=0.3)
                
                # 4. Prompt Engineering
                custom_prompt_template = """You are an expert consultant capable of simplifying complex documents (Legal, Medical, Technical).
                Use the following pieces of context to answer the user's question.
                If you don't know the answer, just say that you don't know, don't try to make up an answer.
                
                Context: {context}
                Question: {question}
                
                Answer (in simple, plain English, highlighting any risks or key points):"""
                
                PROMPT = PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
                
                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=retriever,
                    return_source_documents=True,
                    chain_type_kwargs={"prompt": PROMPT}
                )
                
                # 5. Run Chain
                result = qa_chain.invoke({"query": user_question})
                
                # Display Result
                st.markdown("### 💡 Answer:")
                st.write(result["result"])
                
                # Show Sources (Optional)
                with st.expander("View Source Context"):
                    for i, doc in enumerate(result["source_documents"]):
                        st.markdown(f"**Source {i+1}:**")
                        st.write(doc.page_content)
                        
            except Exception as e:
                st.error(f"An error occurred: {e}")

else:
    st.info("👈 Upload a document in the sidebar to get started!")
