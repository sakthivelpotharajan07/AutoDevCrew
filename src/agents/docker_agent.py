from pathlib import Path

def generate_dockerfile(project_path: str, framework: str = "fastapi"):
    project_dir = Path(project_path)
    # Ensure project directory exists
    if not project_dir.exists():
        project_dir.mkdir(parents=True, exist_ok=True)

    docker_content = ""

    if framework.lower() == "fastapi":
        docker_content = """
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    elif framework.lower() == "flask":
        docker_content = """
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
"""
    
    # Default fallback if framework not matched (could treat as generic python script)
    else:
         docker_content = """
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
"""

    docker_file_path = project_dir / "Dockerfile"
    docker_file_path.write_text(docker_content.strip(), encoding="utf-8")

    return f"Dockerfile created at {docker_file_path}"


def generate_requirements(project_path: str, framework: str = "fastapi"):
    project_dir = Path(project_path)
    # Ensure project directory exists
    if not project_dir.exists():
        project_dir.mkdir(parents=True, exist_ok=True)

    requirements_content = ""

    if framework.lower() == "fastapi":
        requirements_content = """
fastapi
uvicorn
"""

    elif framework.lower() == "flask":
        requirements_content = """
flask
"""
    else:
         requirements_content = """
# Add your requirements here
"""

    requirements_file = project_dir / "requirements.txt"
    
    # Only create if it doesn't exist to avoid overwriting user changes? 
    # The prompt says "Generate requirements.txt (if missing)" in description but code provided overwrites.
    # I will follow the provided code structure but maybe add a check or just overwrite as requested by "Paste this full working version".
    # The prompt code creates it unconditionally. I will stick to the prompt's code logic but add the slight safety of encoding.
    
    requirements_file.write_text(requirements_content.strip(), encoding="utf-8")

    return f"requirements.txt created at {requirements_file}"
