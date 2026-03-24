import json
import re
from src.agents import Agent

class TaskPlannerAgent(Agent):
    def __init__(self):
        super().__init__("TaskPlannerAgent")

    def run(self):
        print(f"[{self.name}] Decomposing requirement into subtasks...")
        requirement = self.orchestrator.state.context.get("requirement", "")
        
        if not requirement:
            print(f"[{self.name}] No requirement found in context.")
            return

        prompt = f"""You are an expert technical project planner.
        User Requirement: "{requirement}"
        
        Break this requirement into a logical, ordered list of technical subtasks.
        
        Return ONLY a JSON array of strings, for example:
        ["Design database schema", "Create API endpoints", "Implement frontend login"]
        
        Do not include any explanation or markdown formatting (like ```json).
        Just the raw JSON array.
        """
        
        # Use the orchestrator's LLM engine
        response = self.orchestrator.llm.generate(prompt)
        
        # Parse the response
        task_plan = self._parse_response(response)
        
        # Store result in context
        self.orchestrator.state.update_context("task_plan", task_plan)
        print(f"[{self.name}] Task planning complete. Generated {len(task_plan)} tasks.")

    def _parse_response(self, response: str) -> list:
        """Parses the LLM response into a list of strings."""
        # Clean up markdown code blocks if present
        clean_response = response.strip()
        if clean_response.startswith("```"):
            # Remove first line (```json or ```) and last line (```)
            lines = clean_response.splitlines()
            if len(lines) >= 2:
                clean_response = "\n".join(lines[1:-1])
        
        try:
            tasks = json.loads(clean_response)
            if isinstance(tasks, list) and all(isinstance(t, str) for t in tasks):
                return tasks
            else:
                print(f"[{self.name}] Warning: valid JSON but not a list of strings.")
                return []
        except json.JSONDecodeError:
            print(f"[{self.name}] Error: Failed to parse JSON response.")
            print(f"Response was: {response}")
            # Fallback: try to split by newlines if it looks like a list
            return [line.strip("- *") for line in clean_response.splitlines() if line.strip()]
