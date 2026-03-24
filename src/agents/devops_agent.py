from src.agents import Agent
import os

class DevOpsAgent(Agent):
    def __init__(self):
        super().__init__("DevOpsAgent")

    def run(self):
        print(f"[{self.name}] Starting CI/CD simulation...")
        
        # Simulate creating artifacts
        code = self.orchestrator.state.context.get("generated_code", "")
        tests = self.orchestrator.state.context.get("tests", "")
        
        build_dir = "src/reports/ci_cd_reports"
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
            
        if isinstance(code, dict):
            code_str = ""
            for filepath, content in code.items():
                code_str += f"\n# --- {filepath} ---\n{content}\n"
        else:
            code_str = str(code) if code else "# No code generated"
            
        if isinstance(tests, dict):
            tests_str = ""
            for testname, content in tests.items():
                tests_str += f"\n# --- {testname} ---\n{content}\n"
        else:
            tests_str = str(tests) if tests else "# No tests generated"
        
        # Mock saving files (legacy artifact)
        try:
            with open(f"{build_dir}/build_artifact.py", "w") as f:
                f.write(code_str)
                
            with open(f"{build_dir}/test_artifact.py", "w") as f:
                f.write(tests_str)
                
            print(f"[{self.name}] Deployment artifacts created at {build_dir}.")
        except Exception as e:
            print(f"[{self.name}] Error saving artifacts: {e}")
            raise e

        # ACTUAL EXTRACTION
        project_dir = "generated_project"
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
            
        print(f"[{self.name}] Extracting generated files to {project_dir}/ ...")
        
        if isinstance(code, dict):
            for filepath, content in code.items():
                target_path = os.path.join(project_dir, filepath)
                # handle subdirectories if required
                target_dir = os.path.dirname(target_path)
                if target_dir and not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                
                try:
                    with open(target_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"[{self.name}] - Saved {filepath}")
                except Exception as e:
                    print(f"[{self.name}] Error saving {filepath}: {e}")

def create_pipeline(code: str) -> str:
    """
    Generates a CI/CD pipeline configuration or validates deployment readiness.
    Intended for direct use by the Editor UI.
    """
    from src.core.llm import LLMEngine
    
    llm = LLMEngine()
    prompt = f"""You are a DevOps Engineer.
    Based on the following Python code, generate a simple CI/CD pipeline configuration (e.g., GitHub Actions YAML).
    
    Also check if the code seems "Deploy Ready" (e.g., has main function, imports look valid).
    
    Output Format:
    ## 🚀 Deployment Status
    [Ready / Needs Work] - Brief explanation.
    
    ## 🛠️ Recommended Pipeline (GitHub Actions)
    ```yaml
    ...
    ```
    
    Code:
    {code}
    """
    
    # Generate response
    response = llm.generate(prompt)
    return response
