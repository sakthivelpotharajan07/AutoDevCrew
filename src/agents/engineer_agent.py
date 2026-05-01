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
        framework = self.orchestrator.state.context.get("framework", "fastapi")
        project_type = self.orchestrator.state.context.get("project_type", "static")
        needs_db = project_type in ["auth", "form"]
        
        extra_instructions = ""
        
        # Smart Prompt Template Engine Logic
        if filepath == "database.py" and needs_db:
            extra_instructions += "Use standard SQLAlchemy declarative_base and sessionmaker. Connect to a local SQLite database EXACTLY at 'sqlite:///./test.db'. Expose engine, SessionLocal, and Base."
        
        elif filepath == "models.py" and needs_db:
            extra_instructions += "Import Base from database. Create an appropriate model (e.g. User or Submission) using SQLAlchemy mapping. Ensure ALL required SQLAlchemy types (e.g., Column, Integer, String, DateTime, Float, ForeignKey, Boolean) and `relationship` are explicitly imported from sqlalchemy. DO NOT use `Column.ForeignKey`, use `ForeignKey` directly. DO NOT create the engine here."
        
        elif filepath == "main.py" and framework == "fastapi":
            extra_instructions += "\nCRITICAL: You are the backend. You must define a FastAPI app named `app`. "
            if needs_db:
                extra_instructions += "CRITICAL DATABASE RULES: You MUST use exactly these database imports: `from database import engine, SessionLocal, Base` and `from models import *`. NEVER import SessionLocal from sqlalchemy! DO NOT redefine database engine or Base in main.py! Execute Base.metadata.create_all(bind=engine). "
            extra_instructions += "You must define a root route `@app.get('/')` that dynamically finds the FIRST `.html` file robustly using absolute paths: `base_dir = Path(__file__).resolve().parent; html_files = list(base_dir.rglob('*.html'))`. Then safely read it: `with open(html_files[0], 'r', encoding='utf-8') as f: return HTMLResponse(content=f.read())`. You MUST forcefully include exactly these core imports at the top (plus any others you need like Pydantic):\n```python\nimport os\nfrom pathlib import Path\nfrom fastapi import FastAPI\nfrom fastapi.responses import HTMLResponse\n```\nCRITICAL: Do NOT just provide the root route; you MUST write fully functional backend API routes (e.g. `/api/...`) that correspond to the frontend UI's fetch calls! DO NOT use relative imports like `from . import models`. DO NOT write uvicorn.run here."
            
        elif filepath == "app.py" and framework == "flask":
            extra_instructions += "\nCRITICAL: You are the backend. You must define a Flask app named `app`. "
            if needs_db:
                extra_instructions += "Import engine, SessionLocal, Base from database. Import ALL models from models. DO NOT redefine engine, Base, or ANY models inside app.py. Include required API routes (use methods=['POST', 'GET']). Execute Base.metadata.create_all(bind=engine). "
            extra_instructions += "You must define a root route `@app.route('/')` that renders `index.html` using `render_template('index.html')`. You MUST import `from flask import Flask, render_template, request, jsonify`. DO NOT write app.run() here."
            
        if filepath.endswith(".html"):
            extra_instructions += "\nCRITICAL: Ensure ALL CSS and JavaScript are written INLINE inside the HTML file using <style> and <script> tags. Do NOT link to external .css or .js files. Ensure you meet the criteria for a premium, dynamic UI design."
            
        if project_type == "api":
            extra_instructions += "\nRULE: Return JSON for API endpoints."
        elif project_type == "form":
            extra_instructions += "\nRULE: Use POST for forms and handle submission dynamically."
            
        extra_instructions += "\nCRITICAL THEMATIC REALISM RULE: You MUST strictly interpret the user's specific domain (e.g. 'clothing', 'hardware', 'cybersecurity'). Do NOT use generic placeholders like 'Product 1', 'Item A', or generic blue/white CSS. You must generate highly customized, visually striking CSS/UI layouts and deeply contextual mock-data (titles, descriptions, prices, images) that perfectly reflect the unique theme of the requirement!"
            
        return f"""You are a senior full-stack software engineer.
        Overall Task: {requirement}
        Project Type: {project_type.capitalize()}
        Framework: {framework.capitalize()}
        
        You are currently implementing the following file:
        File Path: {filepath}
        Description: {description}
        
        Previous Feedback (if any):
        {self.orchestrator.state.context.get("feedback", "None")}
        
        {extra_instructions}
        
        Please generate the code ONLY for this specific file.
        If feedback is provided, ensure you fix the issues mentioned.
        
        Provide ONLY the code. Do not include markdown backticks or explanations. Do not print the language name at the top.
        """
        
    def _clean_code(self, code: str) -> str:
        import re
        code = code.strip()
        # Extract content between ```<lang> and ``` if present
        match = re.search(r'```(?:[a-zA-Z0-9_\-\.]+)?\n(.*?)```', code, re.DOTALL | re.IGNORECASE)
        if match:
            code = match.group(1).strip()
        else:
            # Fallback to stripping basic ticks if no match
            if code.startswith("```"):
                code = re.sub(r'^```[a-zA-Z0-9_\-\.]*\s*\n?', '', code, flags=re.IGNORECASE)
            if code.endswith("```"):
                code = code[:-3]
        
        code = code.strip()
        # Sometimes the LLM outputs the language name on the first line
        lines = code.splitlines()
        if lines and lines[0].strip().lower() in ["python", "html", "css", "javascript", "js", "json", "bash", "sh", "txt", "sql"]:
            lines = lines[1:]
            
        return "\n".join(lines).strip()

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
