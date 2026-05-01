from src.agents import Agent

class TesterAgent(Agent):
    def __init__(self):
        super().__init__("TesterAgent")

    def run(self):
        print(f"[{self.name}] Analyzing code and generating tests...")
        generated_code = self.orchestrator.state.context.get("generated_code", {})
        
        if isinstance(generated_code, dict):
            code_to_test = "Project Files:\n"
            for filepath, content in generated_code.items():
                code_to_test += f"\n--- File: {filepath} ---\n{content}\n"
        else:
            code_to_test = str(generated_code)
        
        prompt = f"""You are a QA tester.
        Code to test:
        {code_to_test}
        
        Please evaluate this code.
        1. Identify the programming language.
        2. If there are FATAL syntax errors or severe logical flaws that would crash the app, return status "FAIL" and explain why in "feedback".
        3. Do NOT fail the code for missing advanced features like "password hashing", "missing register page", "JWT tokens" or "error handling" unless explicitly asked for. This is a basic prototype.
        4. If the code is functionally runnable, return status "PASS" and provide basic unit tests in "tests".
        
        Return ONLY a JSON object with this structure:
        {{
            "status": "PASS" | "FAIL",
            "feedback": "Reason for failure or comments",
            "tests": "Unit test code (if PASS)"
        }}
        """
        
        # Use the orchestrator's LLM engine
        response = self.orchestrator.llm.generate(prompt)
        
        # Simple JSON parsing (robust parsing would use a shared utility)
        import json
        try:
            # Clean markdown
            clean_response = response.strip()
            if clean_response.startswith("```"):
                clean_response = clean_response.split("\n", 1)[1].rsplit("\n", 1)[0]
            
            data = json.loads(clean_response)
            
            self.orchestrator.state.update_context("validation_status", data.get("status", "UNKNOWN"))
            self.orchestrator.state.update_context("feedback", data.get("feedback", ""))
            
            if data.get("status") == "PASS":
                self.orchestrator.state.update_context("tests", data.get("tests", ""))
                print(f"[{self.name}] Validation PASSED.")
            else:
                print(f"[{self.name}] Validation FAILED: {data.get('feedback')}")
                
        except Exception as e:
            print(f"[{self.name}] Error parsing QA response: {e}")
            self.orchestrator.state.update_context("validation_status", "UNKNOWN")
            self.orchestrator.state.update_context("feedback", f"Parse error: {e}")
            
        print(f"[{self.name}] Analysis complete.")

def analyze_code(code: str) -> str:
    """
    Analyzes the given code for bugs, security issues, and improvements.
    Intended for direct use by the Editor UI.
    """
    from src.core.llm import LLMEngine
    
    llm = LLMEngine()
    prompt = f"""You are a QA Lead and Security Expert.
    Please analyze the following code.
    
    Provide a report with:
    1. 🐛 **Potential Bugs**: Logic errors, edge cases.
    2. 🔒 **Security Risks**: Vulnerabilities, unsafe practices.
    3. 💡 **Improvements**: Performance, readability, best practices.
    
    Format the output as clear Markdown with bullet points.
    Be concise but specific. Reference line numbers if possible.
    
    Code:
    {code}
    """
    
    # Generate response
    response = llm.generate(prompt)
    return response
