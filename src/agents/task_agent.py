import json
from src.agents import Agent

class TaskAgent(Agent):
    def __init__(self):
        super().__init__("TaskAgent")

    def run(self):
        print(f"[{self.name}] Classifying project and determining file structure...")
        requirement = self.orchestrator.state.context.get("requirement", "")
        
        if not requirement:
            print(f"[{self.name}] No requirement found in context.")
            return

        # Simple string-based heuristics to suggest framework, backend type
        req_lower = requirement.lower()
        framework = "flask" if "flask" in req_lower else "fastapi"
        
        project_type = "static"
        if any(w in req_lower for w in ["login", "auth", "register", "signup"]):
            project_type = "auth"
        elif any(w in req_lower for w in ["form", "submit", "application"]):
            project_type = "form"
        elif any(w in req_lower for w in ["dashboard", "stock", "chart", "analytics"]):
            project_type = "dashboard"
            
        self.orchestrator.state.update_context("project_type", project_type)
        self.orchestrator.state.update_context("framework", framework)
        
        print(f"[{self.name}] Detected Project Type: {project_type.upper()} | Framework: {framework.upper()}")

        prompt = f"""You are an expert full-stack software architect.
        User Requirement: "{requirement}"
        Target Framework: {framework.capitalize()}
        Project Type: {project_type.capitalize()}
        
        Determine the exact file structure required to implement this requirement.
        
        CRITICAL RULES:
        1. As a full-stack {framework.capitalize()} application, you MUST include:
           - A backend entry point. For FastAPI, name it `main.py`. For Flask, name it `app.py`.
           - EXACTLY ONE frontend HTML file. 
             - If using FastAPI, name it `index.html` (or `login.html`).
             - If using Flask, you MUST place it in a `templates/` folder (e.g., `templates/index.html`).
           - All CSS and JS MUST be inline within the HTML file. DO NOT generate separate `.css` or `.js` files.
           - A `requirements.txt` file containing the framework name ({framework}) and any other required libraries (e.g., sqlalchemy).
        2. Keep the architecture simple, avoiding unnecessary nesting.
        
        Return ONLY a JSON array of objects, where each object has 'path' and 'description'.
        For example:
        [
            {{"path": "app.py", "description": "Flask backend entry point serving the HTML"}},
            {{"path": "templates/index.html", "description": "The main frontend HTML file"}},
            {{"path": "requirements.txt", "description": "{framework}, etc."}}
        ]
        
        Do not include any explanation or markdown formatting (like ```json).
        Just the raw JSON array.
        """
        
        # Use the orchestrator's LLM engine
        response = self.orchestrator.llm.generate(prompt)
        
        # Parse the response
        file_structure = self._parse_response(response)
        
        # Inject database.py and models.py if auth/login/form is detected OR if the LLM decided they were necessary
        heuristic_needs_db = project_type in ["auth", "form"]
        ai_generated_db = any("database.py" in f.get("path", "") or "models.py" in f.get("path", "") for f in file_structure)
        needs_db = heuristic_needs_db or ai_generated_db
        
        # Rule-based requirements mapping
        dependencies = self._extract_requirements(requirement)
        if framework not in dependencies:
            dependencies.add(framework)
            if framework == "fastapi":
                dependencies.add("uvicorn")
                
        if needs_db:
            dependencies.add("sqlalchemy")
            if framework == "fastapi":
                dependencies.add("python-multipart")
                
        if dependencies:
            req_content = "\n".join(sorted(list(dependencies)))
            self.orchestrator.state.update_context("rule_based_requirements", req_content)
            
            # Ensure requirements.txt is in the file structure
            if not any("requirements.txt" in f.get("path", "") for f in file_structure):
                file_structure.append({
                    "path": "requirements.txt",
                    "description": "Project dependencies generated via rule-based mapping"
                })
                
        if needs_db:
            if not any("database.py" in f.get("path", "") for f in file_structure):
                file_structure.append({"path": "database.py", "description": "SQLAlchemy SQLite connection setup"})
            if not any("models.py" in f.get("path", "") for f in file_structure):
                file_structure.append({"path": "models.py", "description": "SQLAlchemy ORM models including User table"})
        
        # Store result in context
        self.orchestrator.state.update_context("file_structure", file_structure)
        print(f"[{self.name}] File structure planning complete. Planned {len(file_structure)} files.")

    def _extract_requirements(self, requirement: str) -> set:
        dependencies = set()
        req_lower = requirement.lower()
        
        mapping = {
            "fastapi": ["fastapi", "uvicorn"],
            "flask": ["flask"],
            "django": ["django"],
            "streamlit": ["streamlit"],
            "pandas": ["pandas"],
            "numpy": ["numpy"],
            "data analysis": ["pandas", "numpy", "matplotlib"],
            "machine learning": ["scikit-learn", "pandas", "numpy"],
            "deep learning": ["torch", "torchvision"],
            "database": ["sqlalchemy"],
            "auth": ["sqlalchemy", "fastapi", "uvicorn"],
            "login": ["sqlalchemy", "fastapi", "uvicorn"],
            "register": ["sqlalchemy", "fastapi", "uvicorn"],
            "mysql": ["mysql-connector-python", "sqlalchemy"],
            "postgres": ["psycopg2-binary", "sqlalchemy"],
            "mongodb": ["pymongo"],
            "api": ["requests"],
            "requests": ["requests"],
            "web scraping": ["beautifulsoup4", "requests"],
            "selenium": ["selenium"],
            "gui": ["tkinter"], 
            "pyqt": ["PyQt5"]
        }
        
        for key, deps in mapping.items():
            if key in req_lower:
                dependencies.update(deps)
                
        return dependencies

    def _parse_response(self, response: str) -> list:
        """Parses the LLM response into a list of dictionaries."""
        # Clean up markdown code blocks if present
        clean_response = response.strip()
        if clean_response.startswith("```"):
            lines = clean_response.splitlines()
            if len(lines) >= 2:
                # find first line without ``` and last line without ```
                if clean_response.startswith("```json"):
                    clean_response = clean_response[7:]
                elif clean_response.startswith("```"):
                    clean_response = clean_response[3:]
                if clean_response.endswith("```"):
                    clean_response = clean_response[:-3]
        
        clean_response = clean_response.strip()
        
        try:
            structure = json.loads(clean_response)
            if isinstance(structure, list) and all(isinstance(t, dict) for t in structure):
                return structure
            else:
                print(f"[{self.name}] Warning: valid JSON but not a list of dictionaries.")
                return []
        except json.JSONDecodeError:
            print(f"[{self.name}] Error: Failed to parse JSON response.")
            print(f"Response was: {response}")
            return []
