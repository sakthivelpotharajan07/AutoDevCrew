import torch
from transformers import pipeline
import warnings
from google import genai
from src.core.utils import load_config, setup_logging
import os

logger = setup_logging("LLM_Engine")

class LLMEngine:
    def __init__(self):
        self.config = load_config()
        self.pipe = None
        self.genai_client = None
        self.provider = self.config["llm"].get("provider", "local")

    def load_model(self):
        if self.provider == "gemini":
            self._load_gemini()
        elif self.provider == "groq":
            self._load_groq()
        else:
            self._load_local()

    def _load_gemini(self):
        if self.genai_client:
            return

        api_key = self.config["llm"].get("api_key")
        if not api_key or api_key == "YOUR_GEMINI_API_KEY":
             # Fallback to env var if config is placeholder
             api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            logger.error("Gemini API key not found in config or environment.")
            print("DEBUG: Gemini API key missing.")
            return

        try:
            self.genai_client = genai.Client(api_key=api_key)
            self.gemini_model_name = self.config["llm"].get("model_id", "gemini-1.5-flash")
            logger.info("Gemini client loaded successfully.")
            print("DEBUG: Gemini client loaded.")
        except Exception as e:
             logger.error(f"Failed to load Gemini: {e}")
             print(f"DEBUG: Failed to load Gemini: {e}")

    def _load_groq(self):
        if hasattr(self, 'groq_client') and self.groq_client:
            return

        api_key = self.config["llm"].get("api_key")
        if not api_key:
            logger.error("Groq API key not found.")
            return

        try:
            from groq import Groq
            self.groq_client = Groq(api_key=api_key)
            logger.info("Groq client loaded successfully.")
        except ImportError:
            logger.error("groq package not found. Please pip install groq")
        except Exception as e:
            logger.error(f"Failed to load Groq: {e}")

    def _load_local(self):
        if self.pipe:
            return

        model_id = self.config["llm"]["model_id"]
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"DEBUG: Loading local model {model_id} on {device}...")
        logger.info(f"Loading local model {model_id} on {device}...")
        try:
            self.pipe = pipeline(
                "text-generation",
                model=model_id,
                device_map="auto" if device == "cuda" else None,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            )
            print("DEBUG: Local Model loaded successfully.")
            logger.info("Local Model loaded successfully.")
        except Exception as e:
            print(f"DEBUG: Failed to load local model: {e}")
            logger.error(f"Failed to load local model {model_id}: {e}")
            self.pipe = None

    def generate(self, prompt: str, max_new_tokens=256):
        if self.provider == "gemini":
            return self._generate_gemini(prompt)
        elif self.provider == "groq":
            return self._generate_groq(prompt)
        else:
            return self._generate_local(prompt, max_new_tokens)

    def _generate_gemini(self, prompt: str):
        if not self.genai_client:
            self.load_model()
        
        if not self.genai_client:
            return "Error: Gemini client not loaded (check API key)."

        try:
            print("DEBUG: Sending request to Gemini...")
            response = self.genai_client.models.generate_content(
                model=self.gemini_model_name,
                contents=prompt
            )
            print("DEBUG: Gemini response received.")
            return response.text
        except Exception as e:
             logger.error(f"Gemini generation error: {e}")
             return f"Error calling Gemini: {e}"

    def _generate_groq(self, prompt: str):
        if not hasattr(self, 'groq_client') or not self.groq_client:
            self.load_model()
        
        if not hasattr(self, 'groq_client') or not self.groq_client:
            return "Error: Groq client not loaded."

        try:
            model_id = self.config["llm"].get("model_id", "mixtral-8x7b-32768")
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model_id,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            return f"Error calling Groq: {e}"

    def _generate_local(self, prompt: str, max_new_tokens=256):
        print("DEBUG: Local Generate request received.")
        if not self.pipe:
            print("DEBUG: Model not loaded, attempting to load...")
            self.load_model()
            
        if not self.pipe:
            return "Error: Local model not loaded."
        
        print("DEBUG: Starting local generation...")
        sequences = self.pipe(
            prompt,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=self.pipe.tokenizer.eos_token_id,
            max_new_tokens=max_new_tokens,
            return_full_text=False, 
        )
        print("DEBUG: Local Generation complete.")
        return sequences[0]['generated_text']
