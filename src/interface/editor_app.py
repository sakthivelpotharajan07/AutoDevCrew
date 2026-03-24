import streamlit as st
import sys
import os
import time
from pathlib import Path

# Ensure project root is in path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import AFTER path adjustment
from streamlit_monaco import st_monaco
from src.agents.engineer_agent import refine_code
from src.agents.tester_agent import analyze_code
from src.agents.devops_agent import create_pipeline
from src.agents.docker_agent import generate_dockerfile, generate_requirements
from src.agents.github_agent import push_to_github

def render_editor():
    """
    Renders the Monaco Code Editor Interface.
    Can be imported and used in other Streamlit apps.
    """
    st.title("🧠 AutoDevCrew – Code Editor")

    # ---------- Sidebar ----------
    st.sidebar.header("📂 Project Files")

    # 1. Check for Generated Code in Session State
    file_options = []
    
    if "generated_code" in st.session_state:
        gen_code = st.session_state.generated_code
        if isinstance(gen_code, dict):
            for k in gen_code.keys():
                file_options.append(f"✨ Generated: {k}")
        else:
            file_options.append("✨ Generated Code")
        
    # 2. Load Project Files
    py_files = []
    file_map = {}
    try:
        py_files = [
            f for f in PROJECT_ROOT.rglob("*.py") 
            if "venv" not in str(f) and ".git" not in str(f) and "__pycache__" not in str(f)
        ]
        file_map = {str(f.relative_to(PROJECT_ROOT)): f for f in py_files}
        
        if file_map:
            file_options.extend(list(file_map.keys()))
        else:
            st.warning("No Python files found in project root.")
            
    except Exception as e:
        st.sidebar.error(f"Error scanning files: {e}")

    # 3. File Selector
    if file_options:
        selected_file = st.sidebar.selectbox(
            "Select a file to edit",
            file_options
        )
    else:
        selected_file = None

    if selected_file:
        # ---------- Load File Content ----------
        code_content = ""
        is_generated = False
        
        if selected_file == "✨ Generated Code":
            is_generated = True
            code_content = st.session_state.generated_code
        elif selected_file.startswith("✨ Generated: "):
            is_generated = True
            file_key = selected_file.replace("✨ Generated: ", "")
            code_content = st.session_state.generated_code.get(file_key, "")
        else:
            file_path = file_map[selected_file]
            try:
                code_content = file_path.read_text(encoding="utf-8")
            except Exception as e:
                st.error(f"Error reading file: {e}")
                code_content = ""

        # ---------- Monaco Editor ----------
        # Store code in session state to handle updates from Agent
        # Reset editor content if file selection changes
        if "editor_code" not in st.session_state or st.session_state.get('current_file') != selected_file:
            st.session_state.editor_code = code_content
            st.session_state.current_file = selected_file

        edited_code = st_monaco(
            value=st.session_state.editor_code,
            language="python",
            theme="vs-dark",
            height=600
        )

        # ---------- Buttons ----------
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if is_generated:
                # For generated code, always allow saving as a new file
                with st.popover("💾 Save to File"):
                    st.markdown("### Save Generated Code")
                    
                    default_path = "src/generated_script.py"
                    if selected_file.startswith("✨ Generated: "):
                        default_path = selected_file.replace("✨ Generated: ", "")
                        
                    new_filename = st.text_input("Destination Path:", value=default_path)
                    if st.button("Confirm Save"):
                        try:
                            save_path = PROJECT_ROOT / new_filename
                            # Ensure directory exists
                            save_path.parent.mkdir(parents=True, exist_ok=True)
                            
                            content_to_save = edited_code if edited_code else st.session_state.editor_code
                            if isinstance(content_to_save, dict):
                                content_to_save = str(content_to_save)
                                
                            save_path.write_text(content_to_save, encoding="utf-8")
                            st.success(f"Saved to {new_filename}")
                            # We might want to switch the selection to the new file, but for now just notify
                            time.sleep(1) # Give user time to see success
                            st.rerun() 
                        except Exception as e:
                            st.error(f"Failed to save: {e}")
            else:
                # Existing file
                if st.button("💾 Save File"):
                    try:
                        content_to_save = edited_code if edited_code else st.session_state.editor_code
                        file_map[selected_file].write_text(content_to_save, encoding="utf-8")
                        st.success(f"File saved: {selected_file}")
                    except Exception as e:
                        st.error(f"Failed to save: {e}")
                
                # option to save as
                with st.popover("Save As..."):
                     st.markdown("### Save Copy")
                     new_filename = st.text_input("New Filename:", value=f"copy_{Path(selected_file).name}")
                     if st.button("Save Copy"):
                        try:
                            save_path = PROJECT_ROOT / new_filename
                            save_path.parent.mkdir(parents=True, exist_ok=True)
                            content_to_save = edited_code if edited_code else st.session_state.editor_code
                            save_path.write_text(content_to_save, encoding="utf-8")
                            st.success(f"Saved copy to {new_filename}")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                             st.error(f"Failed to save: {e}")

        with col2:
            if st.button("▶️ Run Code"):
                if not edited_code and not code_content:
                    st.warning("No code to run.")
                else:
                    with st.spinner("Running code..."):
                        import subprocess
                        import tempfile
                        
                        code_to_run = edited_code if edited_code else st.session_state.editor_code
                        if isinstance(code_to_run, dict):
                            code_to_run = str(code_to_run)
                        
                        # Fix: Determine execution directory so relative imports work
                        exec_dir = PROJECT_ROOT / "generated_project"
                        exec_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Fix: Check dependencies before execution
                        req_path = exec_dir / "requirements.txt"
                        if req_path.exists():
                           subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_path)], cwd=str(exec_dir))
                        
                        # Try to use original filename if known to preserve module logic, else default tmp.
                        filename = "run_temp.py"
                        if st.session_state.get('current_file') and not st.session_state.get('current_file').startswith("✨"):
                            filename = Path(st.session_state.current_file).name
                        elif hasattr(st.session_state, 'current_file') and "✨ Generated: " in st.session_state.current_file:
                            filename = st.session_state.current_file.replace("✨ Generated: ", "")
                            
                        tmp_path = exec_dir / f"tmp_{filename}"
                        
                        try:
                            tmp_path.write_text(code_to_run, encoding="utf-8")
                            
                            if tmp_path.suffix != ".py":
                                st.session_state.terminal_output = f"File {filename} is a static or non-Python file and cannot be executed natively."
                                st.session_state.terminal_error = ""
                                st.session_state.exec_time = "0.0s"
                                st.session_state.exit_code = 0
                            else:
                                env = os.environ.copy()
                                env["PYTHONPATH"] = str(exec_dir)
                                
                                # Run the script and capture output
                                start_time = time.time()
                                result = subprocess.run(
                                    [sys.executable, str(tmp_path)],
                                    capture_output=True,
                                    text=True,
                                    timeout=30, # 30 second timeout max
                                    cwd=str(exec_dir),
                                    env=env
                                )
                                end_time = time.time()
                                
                                st.session_state.terminal_output = result.stdout
                                st.session_state.terminal_error = result.stderr
                                st.session_state.exec_time = f"{end_time - start_time:.2f}s"
                                st.session_state.exit_code = result.returncode
                        except subprocess.TimeoutExpired:
                            st.session_state.terminal_output = ""
                            st.session_state.terminal_error = "Execution timed out (Limit: 30s)."
                            st.session_state.exec_time = ">30s"
                            st.session_state.exit_code = -1
                        except Exception as e:
                           st.session_state.terminal_output = ""
                           st.session_state.terminal_error = f"Error launching process: {e}"
                           st.session_state.exec_time = "N/A"
                           st.session_state.exit_code = -1
                        finally:
                            # Clean up the temp file
                            try:
                                if tmp_path.exists():
                                    tmp_path.unlink()
                            except:
                                pass
                                
        # Terminal Output Area
        st.markdown("---")
        st.markdown("### 🖥️ Terminal Output")
        
        # Determine styling and content based on state
        term_out = st.session_state.get("terminal_output", "")
        term_err = st.session_state.get("terminal_error", "")
        exec_time = st.session_state.get("exec_time", "")
        exit_code = st.session_state.get("exit_code", None)
        
        if exit_code is not None:
            if exit_code == 0:
                st.success(f"Execution finished in {exec_time}")
            else:
                st.error(f"Execution failed with exit code {exit_code} in {exec_time}")
                
        # Use a disabled text area to simulate a terminal pane
        combined_output = "No output yet."
        if term_out or term_err:
            combined_output = ""
            if term_out:
                combined_output += f"--- STDOUT ---\n{term_out}\n"
            if term_err:
                combined_output += f"--- STDERR ---\n{term_err}\n"
                
        st.code(combined_output, language="bash")
        with col3:
            if st.button("🐳 Generate Docker"):
                try:
                    result1 = generate_requirements("generated_project", "fastapi")
                    result2 = generate_dockerfile("generated_project", "fastapi")
                    st.success(result1)
                    st.success(result2)
                except Exception as e:
                    st.error(f"Docker generation failed: {e}")

        with col4:
            if st.button("🚀 Push to GitHub"):
                # You might want to make 'repo_name' dynamic or input based
                # For now using a hardcoded default or user input could optionally be added
                result = push_to_github("generated_project", "login-system-demo")
                if "Error" in result:
                     st.error(result)
                else:
                     st.success(result)

    else:
        st.info("Please select a file from the sidebar to start editing.")

if __name__ == "__main__":
    st.set_page_config(page_title="AutoDevCrew Editor", layout="wide")
    render_editor()
