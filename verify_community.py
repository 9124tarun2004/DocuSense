try:
    from langchain.chains import RetrievalQA
    print("Original import works (Unexpected)")
except ImportError:
    try:
        from langchain_community.chains import RetrievalQA
        print("SUCCESS: RetrievalQA found in langchain_community")
    except ImportError as e:
        print(f"FAILURE: {e}")
