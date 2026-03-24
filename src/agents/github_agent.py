import os
import subprocess
from pathlib import Path

def push_to_github(project_path: str, repo_name: str):
    project_dir = Path(project_path)

    github_username = os.getenv("GITHUB_USERNAME")
    github_token = os.getenv("GITHUB_TOKEN")

    if not github_username or not github_token:
        return "GitHub credentials not set."

    remote_url = f"https://{github_username}:{github_token}@github.com/{github_username}/{repo_name}.git"

    try:
        # Check if git is already initialized
        if not (project_dir / ".git").exists():
            subprocess.run(["git", "init"], cwd=project_dir, check=False)
        
        # Configure user if not set (optional, good practice for automated commits)
        # subprocess.run(["git", "config", "user.email", "autodevcrew@example.com"], cwd=project_dir, check=False)
        # subprocess.run(["git", "config", "user.name", "AutoDevCrew"], cwd=project_dir, check=False)

        subprocess.run(["git", "add", "."], cwd=project_dir, check=False)
        subprocess.run(["git", "commit", "-m", "Initial commit by AutoDevCrew"], cwd=project_dir, check=False)
        subprocess.run(["git", "branch", "-M", "main"], cwd=project_dir, check=False)
        
        # Remove existing origin if any to avoid errors on retry
        subprocess.run(["git", "remote", "remove", "origin"], cwd=project_dir, check=False)
        
        subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=project_dir, check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=project_dir, check=True)

        return f"Project pushed to GitHub repo: {repo_name}"

    except Exception as e:
        return f"Error pushing to GitHub: {str(e)}"
