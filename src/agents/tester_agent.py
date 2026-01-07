from src.agents import Agent

class TesterAgent(Agent):
    def __init__(self):
        super().__init__("TesterAgent")

    def run(self):
        print(f"[{self.name}] Generating tests...")
        code = self.orchestrator.state.context.get("generated_code", "")
        
        if not code:
            print(f"[{self.name}] No code found to test.")
            return

        code_preview = code[:800] if len(code) > 800 else code

        prompt = f"""<|system|>
You are a QA expert. Write pytest tests for the code below. Return ONLY code.
</s>
<|user|>
Code:
{code_preview}
</s>
<|assistant|>
"""
        
        tests = self.orchestrator.llm.generate(prompt)
        self.orchestrator.state.update_context("tests", tests)
        self.orchestrator.memory.add_memory(tests, {"type": "test", "source": "TesterAgent"})
        
        print(f"[{self.name}] Tests generated.")
