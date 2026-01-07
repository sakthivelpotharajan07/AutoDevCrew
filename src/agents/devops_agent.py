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
        
        # Mock saving files
        try:
            with open(f"{build_dir}/build_artifact.py", "w") as f:
                f.write(code if code else "# No code generated")
                
            with open(f"{build_dir}/test_artifact.py", "w") as f:
                f.write(tests if tests else "# No tests generated")
                
            print(f"[{self.name}] Deployment artifacts created at {build_dir}.")
        except Exception as e:
            print(f"[{self.name}] Error saving artifacts: {e}")
            raise e
