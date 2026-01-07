import google.generativeai as genai
from src.core.utils import load_config
import sys

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

try:
    config = load_config()
    api_key = config["llm"].get("api_key")
    genai.configure(api_key=api_key)

    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
             print(m.name)
except Exception as e:
    print(f"Error: {e}")
