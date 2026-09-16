import sys
from pathlib import Path

# Add project root to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from llm.gemini_client import GeminiClient

llm = GeminiClient()

response = llm.generate("What is Artificial Intelligence?")

print(response)
