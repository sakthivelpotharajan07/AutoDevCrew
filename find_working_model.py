import google.generativeai as genai
from src.core.utils import load_config
import sys

# clean stdout
sys.stdout.reconfigure(encoding='utf-8')

config = load_config()
api_key = config["llm"].get("api_key")
genai.configure(api_key=api_key)

candidates = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-1.0-pro",
    "gemini-pro",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro", 
    "models/gemini-1.0-pro"
]

print("Testing models...")
found = False
for model_name in candidates:
    print(f"Testing: {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        print(f"SUCCESS: {model_name}")
        found = True
        break 
    except Exception as e:
        # short error
        err = str(e).split('\n')[0]
        print(f"FAILED: {model_name} - {err}")

if not found:
    print("ALL FAILED.")
