import tempfile, subprocess, sys, os

code_to_run = """
import sys
print("Starting...", file=sys.stderr)
import nonexistent_module  # this should throw ModuleNotFoundError
"""

with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tmp:
    tmp.write(code_to_run)
    tmp_path = tmp.name

try:
    result = subprocess.run(
        [sys.executable, tmp_path],
        capture_output=True,
        text=True,
        timeout=30
    )
    print("Return code:", result.returncode)
    print("Stdout:", repr(result.stdout))
    print("Stderr:", repr(result.stderr))
finally:
    os.unlink(tmp_path)
