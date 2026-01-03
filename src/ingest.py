import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Define paths
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')
DB_FAISS_PATH = os.path.join(os.path.dirname(__file__), '..', 'vectorstore', 'db_faiss')

def create_vector_db(uploaded_file=None):
    """
    Creates a vector database from a PDF file.
    If uploaded_file is provided, it processes that file.
    Otherwise, it looks for files in the DATA_PATH.
    """
    
    # If a file is uploaded via Streamlit, save it temporarily
    if uploaded_file:
        file_path = os.path.join(DATA_PATH, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        pdf_file = file_path
    else:
        # For manual testing, just grab the first PDF in data folder
        files = [f for f in os.listdir(DATA_PATH) if f.endswith('.pdf')]
        if not files:
            return None
        pdf_file = os.path.join(DATA_PATH, files[0])

    # 1. Load the PDF
    loader = PyPDFLoader(pdf_file)
    documents = loader.load()

    # 2. Split Text (Chunking)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # 3. Create Embeddings (Hugging Face)
    # Using 'all-MiniLM-L6-v2' which is small and fast for CPU
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    # 4. Create Vector Store (FAISS)
    db = FAISS.from_documents(texts, embeddings)
    
    # Save locally
    db.save_local(DB_FAISS_PATH)
    
    return db

def get_vector_db():
    """Loads the existing FAISS index."""
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})
    if os.path.exists(DB_FAISS_PATH):
        db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
        return db
    return None

if __name__ == "__main__":
    create_vector_db()
