from src.agents import Agent
import os

class SummarizerAgent(Agent):
    def __init__(self):
        super().__init__("SummarizerAgent")

    def run(self):
        print(f"[{self.name}] Summarizing session...")
        state = self.orchestrator.state
        
        summary = f"""
        # Session Summary
        Status: {state.status.name}
        Context Keys: {list(state.context.keys())}
        Errors: {state.errors}
        """
        
        output_path = "src/reports/daily_reports/latest_summary.md"
        output_dir = os.path.dirname(output_path)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        try:
            with open(output_path, "w") as f:
                f.write(summary)
            print(f"[{self.name}] Summary saved.")
        except Exception as e:
            print(f"[{self.name}] Failed to save summary: {e}")
            # Non-critical, don't crash pipeline? 
            # But prompt says it ends with FAILED so maybe we should let it pass or log error to state?
            state.errors.append(f"Summarizer failed: {e}")
