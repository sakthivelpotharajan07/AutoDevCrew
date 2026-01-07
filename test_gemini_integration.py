from src.core.llm import LLMEngine
import sys

try:
    print("Initializing Engine...")
    engine = LLMEngine()
    print(f"Provider: {engine.provider}")
    print("Attempting generation (expect failure if no API key)...")
    result = engine.generate("Hello, are you working?")
    print(f"Result: {result}")
except Exception as e:
    print(f"Caught expected exception or error: {e}")
