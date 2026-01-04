try:
    from langchain.chains import RetrievalQA
    print("SUCCESS: RetrievalQA imported")
except ImportError as e:
    print(f"FAILURE: {e}")
    import langchain
    print(f"LangChain Version: {langchain.__version__}")
