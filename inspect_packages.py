
import langchain
import langchain_community
import pkgutil

print("--- LangChain Dir ---")
print(dir(langchain))

print("\n--- LangChain Community Dir ---")
print(dir(langchain_community))

print("\n--- LangChain Submodules ---")
# Attempt to list submodules
try:
    for importer, modname, ispkg in pkgutil.iter_modules(langchain.__path__):
        print(f"langchain.{modname}")
except Exception as e:
    print(e)
