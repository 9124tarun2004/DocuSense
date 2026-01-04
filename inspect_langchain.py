
import sys
import pkgutil
import langchain
import langchain_community

print(f"LangChain Path: {langchain.__path__}")
print(f"LangChain Community Path: {langchain_community.__path__}")

# Try to find 'chains' in langchain
try:
    import langchain.chains
    print("SUCCESS: import langchain.chains")
except ImportError as e:
    print(f"FAILURE: import langchain.chains: {e}")

# Try to find RetrievalQA in langchain_community
try:
    from langchain_community.chains import RetrievalQA
    print("SUCCESS: from langchain_community.chains import RetrievalQA")
except ImportError as e:
    print(f"FAILURE: from langchain_community.chains import RetrievalQA: {e}")

# Try generic search for RetrievalQA
import inspect
def find_symbol(module, symbol_name):
    if hasattr(module, symbol_name):
        return f"{module.__name__}.{symbol_name}"
    return None

print("Searching for RetrievalQA...")
found = False
# Check langchain root
if hasattr(langchain, "RetrievalQA"):
    print("Found in langchain.RetrievalQA")
    found = True

# Check chains if it existed (failed import suggests no, but maybe submodules?)

# Check community
if hasattr(langchain_community, "RetrievalQA"):
    print("Found in langchain_community.RetrievalQA")
    found = True
    
try:
    import langchain.chains as lc_chains
    if hasattr(lc_chains, "RetrievalQA"):
        print("Found in langchain.chains.RetrievalQA")
        found = True
except:
    pass

if not found:
    print("RetrievalQA not found in top levels.")

