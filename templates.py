import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    f"src/agents/__init__.py",
    f"src/agents/engineer_agent.py",
    f"src/agents/tester_agent.py",
    f"src/agents/devops_agent.py",
    f"src/agents/summarizer_agent.py",
    f"src/core/coordinator.py",
    f"src/core/memory_manager.py",
    f"src/core/inference_engine.py",
    f"src/core/utils.py",
    f"src/core/__init__.py",
    f"src/interface/dashboard_app.py",
    f"src/interface/api_server.py",
    f"src/interface/__init__.py",
    f"src/reports/daily_reports/",
    f"src/reports/test_logs/",
    f"src/reports/ci_cd_reports/",
    f"main.py",
    f"config.yaml",
    f"README.md",
    f"__init__.py",
    f"models/ollama/",
    f"models/huggingface/",
    f"data/memory.db",
    f"data/chromadb/",
    f"tests/test_engineer_agent.py",
    f"tests/test_tester_agent.py",
    f"tests/test_pipeline.py",
    f"deployment.requirements.txt",
    f"deployment/app_start.sh",
    f"deployment/README.md"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating Directory: {filedir} for the file : {filename}")
    if (not os.path.exists(filepath) or (os.path.getsize(filepath)) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} is already exists")
