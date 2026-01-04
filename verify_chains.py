
try:
    import langchain.chains
    print("SUCCESS: import langchain.chains")
except ImportError as e:
    print(f"FAILURE: import langchain.chains: {e}")

try:
    from langchain.chains import RetrievalQA
    print("SUCCESS: from langchain.chains import RetrievalQA")
except ImportError as e:
    print(f"FAILURE: from langchain.chains import RetrievalQA: {e}")

try:
    from langchain_community.chains import RetrievalQA
    print("SUCCESS: from langchain_community.chains import RetrievalQA")
except ImportError as e:
    print(f"FAILURE: from langchain_community.chains import RetrievalQA: {e}")

try:
    from langchain.chains import create_retrieval_chain
    print("SUCCESS: from langchain.chains import create_retrieval_chain")
except ImportError as e:
    print(f"FAILURE: from langchain.chains import create_retrieval_chain: {e}")
