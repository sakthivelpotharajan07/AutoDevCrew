from src.agents import Agent

class EngineerAgent(Agent):
    def __init__(self):
        super().__init__("EngineerAgent")

    def run(self):
        print(f"[{self.name}] Analyzing requirements...")
        context = self.orchestrator.state.context.get("requirement", "")
        
        # Very simple prompt for TinyLlama with explicit instruction
        prompt = f"""<|system|>
You are a Python expert. Return ONLY valid Python code.
IMPORTANT: Write functions that RETURN values, do not just print.
</s>
<|user|>
Write a python program for: {context}
</s>
<|assistant|>
"""
        print(f"DEBUG: Final Prompt: {prompt}")
        
        generated_code = self.orchestrator.llm.generate(prompt)
        
        self.orchestrator.state.update_context("generated_code", generated_code)
        self.orchestrator.memory.add_memory(generated_code, {"type": "code", "source": "EngineerAgent"})
        
        print(f"[{self.name}] Code generated.")
