try:
    import langchain_google_genai
    print(f"SUCCESS: langchain_google_genai imported. File: {langchain_google_genai.__file__}")
except ImportError as e:
    print(f"FAILURE: {e}")
except Exception as e:
    print(f"ERROR: {e}")
