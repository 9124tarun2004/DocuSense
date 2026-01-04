
import sys
import os

print(f"Python Executable: {sys.executable}")

try:
    import langchain
    print(f"SUCCESS: langchain imported (Version: {getattr(langchain, '__version__', 'unknown')})")
except ImportError as e:
    print(f"FAILURE: langchain not found: {e}")

try:
    import faiss
    print(f"SUCCESS: faiss imported")
except ImportError as e:
    print(f"FAILURE: faiss not found: {e}")

try:
    import langchain_community
    print(f"SUCCESS: langchain_community imported")
except ImportError as e:
    print(f"FAILURE: langchain_community not found: {e}")
