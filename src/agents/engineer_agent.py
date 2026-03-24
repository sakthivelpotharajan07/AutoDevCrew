from src.agents import Agent

class EngineerAgent(Agent):
    def __init__(self):
        super().__init__("EngineerAgent")

    def run(self):
        print(f"[{self.name}] Analyzing requirement and generating code...")
        requirement = self.orchestrator.state.context.get("requirement", "")
        file_structure = self.orchestrator.state.context.get("file_structure", [])
        
        generated_code_dict = {}
        
        if not file_structure:
            print(f"[{self.name}] No file structure found, generating single file.")
            # Fallback to single file generation
            prompt = self._build_prompt(requirement, "main.py", "Main logic")
            response = self.orchestrator.llm.generate(prompt)
            generated_code_dict["main.py"] = self._clean_code(response)
        else:
            print(f"[{self.name}] Found {len(file_structure)} files to generate.")
            for file_info in file_structure:
                filepath = file_info.get("path", "unknown.py")
                description = file_info.get("description", "")
                
                # Rule-based generation for requirements.txt
                if filepath == "requirements.txt" and self.orchestrator.state.context.get("rule_based_requirements"):
                    print(f"[{self.name}] Using rule-based generator for {filepath}...")
                    generated_code_dict[filepath] = self.orchestrator.state.context.get("rule_based_requirements")
                    continue

                print(f"[{self.name}] Generating code for {filepath}...")
                
                prompt = self._build_prompt(requirement, filepath, description)
                response = self.orchestrator.llm.generate(prompt)
                generated_code_dict[filepath] = self._clean_code(response)
        
        # Store result in context
        self.orchestrator.state.update_context("generated_code", generated_code_dict)
        print(f"[{self.name}] Code generation complete.")

    def _build_prompt(self, requirement: str, filepath: str, description: str) -> str:
        extra_instructions = ""
        req_lower = requirement.lower()
        needs_db = any(w in req_lower for w in ["login", "database", "auth", "register", "signup"])
        
        if filepath == "database.py" and needs_db:
            extra_instructions = "Use standard SQLAlchemy declarative_base and sessionmaker. Connect to a local SQLite database 'sqlite:///./test.db'."
        elif filepath == "models.py" and needs_db:
            extra_instructions = "Create a User model with id, username, and password using SQLAlchemy mapping."
        elif "main.py" in filepath and needs_db:
            extra_instructions = "Include FastAPI routing for /register and /login using SQLAlchemy Session dependency. Also execute Base.metadata.create_all(bind=engine) to create tables automatically."
            
        return f"""You are a senior software engineer.
        Overall Task: {requirement}
        
        You are currently implementing the following file:
        File Path: {filepath}
        Description: {description}
        
        First, identify the programming language required for this task. 
        If not explicitly stated, infer it from the context and extension.
        
        Target Language: <Inferred Language>
        
        Previous Feedback (if any):
        {self.orchestrator.state.context.get("feedback", "None")}
        
        {extra_instructions}
        
        Please generate the code ONLY for this specific file.
        If feedback is provided, ensure you fix the issues mentioned.
        
        Provide ONLY the code. Do not include markdown backticks or explanations.
        """
        
    def _clean_code(self, code: str) -> str:
        import re
        code = code.strip()
        # Extract content between ```<lang> and ``` if present
        match = re.search(r'```(?:[a-zA-Z0-9_\-\.]+)?\n(.*?)```', code, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        # Fallback to stripping basic ticks if no match
        if code.startswith("```"):
            code = re.sub(r'^```[a-zA-Z0-9_\-\.]*\s*\n?', '', code, flags=re.IGNORECASE)
        if code.endswith("```"):
            code = code[:-3]
        return code.strip()

def refine_code(code: str) -> str:
    """
    Refines the given code using the LLM. 
    Intended for direct use by the Editor UI.
    """
    from src.core.llm import LLMEngine
    
    llm = LLMEngine()
    prompt = f"""You are a senior software engineer.
    Please improve or refine the following code. 
    - Fix potential bugs
    - Improve readability
    - Add type hints if missing
    - Optimize where appropriate
    
    RETURN ONLY THE CODE between start/end markers or plain text. 
    DO NOT wrap in markdown code blocks if possible, or minimally wrap.
    
    Code:
    {code}
    """
    
    # Generate response
    response = llm.generate(prompt)
    
    import re
    response = response.strip()
    match = re.search(r'```(?:[a-zA-Z0-9_\-\.]+)?\n(.*?)```', response, re.DOTALL | re.IGNORECASE)
    if match:
        response = match.group(1).strip()
    else:
        if response.startswith("```"):
            response = re.sub(r'^```[a-zA-Z0-9_\-\.]*\s*\n?', '', response, flags=re.IGNORECASE)
        if response.endswith("```"):
            response = response[:-3]
            
    return response.strip()
