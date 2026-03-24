import os
from groq import Groq
from src.core.utils import load_config

try:
    config = load_config()
    api_key = config["llm"].get("api_key")
    
    if not api_key:
        print("Error: No API key found in config")
        exit(1)

    client = Groq(api_key=api_key)
    models = client.models.list()
    
    print("\nAvailable Groq Models:")
    for model in models.data:
        print(f"- {model.id}")
        
except Exception as e:
    print(f"Error: {e}")
