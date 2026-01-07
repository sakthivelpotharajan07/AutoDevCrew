import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import uvicorn
import subprocess
from src.core.orchestrator import Orchestrator
from src.agents.engineer_agent import EngineerAgent
from src.agents.tester_agent import TesterAgent
from src.agents.devops_agent import DevOpsAgent
from src.agents.summarizer_agent import SummarizerAgent

def run_cli(requirement):
    orchestrator = Orchestrator()
    orchestrator.register_agent(EngineerAgent())
    orchestrator.register_agent(TesterAgent())
    orchestrator.register_agent(DevOpsAgent())
    orchestrator.register_agent(SummarizerAgent())
    
    orchestrator.run_pipeline(requirement)

def start_api():
    # Use 'src.interface.api_server:app' which requires 'src' in path (added above)
    uvicorn.run("src.interface.api_server:app", host="0.0.0.0", port=8000, reload=True)

def start_dashboard():
    # Streamlit runs as options, we need to ensure it has PYTHONPATH or runs from root
    env = os.environ.copy()
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env["PYTHONPATH"] = root_dir
    
    dashboard_path = os.path.join(root_dir, "src", "interface", "dashboard_app.py")
    
    subprocess.run(["streamlit", "run", dashboard_path], env=env)

def main():
    parser = argparse.ArgumentParser(description="AutoDevCrew CLI")
    parser.add_argument("mode", choices=["cli", "api", "dashboard"], help="Mode to run")
    parser.add_argument("--req", help="Requirement for CLI mode")
    
    args = parser.parse_args()
    
    if args.mode == "cli":
        if not args.req:
            print("Error: --req is required for CLI mode")
            return
        run_cli(args.req)
    elif args.mode == "api":
        start_api()
    elif args.mode == "dashboard":
        start_dashboard()

if __name__ == "__main__":
    main()
