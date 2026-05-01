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

        # ---------- Sleek Action Bar ----------
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🛠️ Editor Actions")
        
        # Use full-width columns for action buttons
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if is_generated:
                with st.popover("💾 Save Snippet", use_container_width=True):
                    st.markdown("**Deploy to Workspace**")
                    default_path = "src/generated_script.py"
                    if selected_file.startswith("✨ Generated: "):
                        default_path = selected_file.replace("✨ Generated: ", "")
                        
                    new_filename = st.text_input("Target Filepath", value=default_path)
                    if st.button("Commit Code"):
                        try:
                            save_path = PROJECT_ROOT / new_filename
                            save_path.parent.mkdir(parents=True, exist_ok=True)
                            
                            content_to_save = edited_code if edited_code else st.session_state.editor_code
                            if isinstance(content_to_save, dict):
                                content_to_save = str(content_to_save)
                                
                            save_path.write_text(content_to_save, encoding="utf-8")
                            st.success(f"Deployed ✅")
                            time.sleep(1)
                            st.rerun() 
                        except Exception as e:
                            st.error(f"Save Failed: {e}")
            else:
                if st.button("💾 Overwrite File", use_container_width=True):
                    try:
                        content_to_save = edited_code if edited_code else st.session_state.editor_code
                        file_map[selected_file].write_text(content_to_save, encoding="utf-8")
                        st.success(f"Overwritten ✅")
                    except Exception as e:
                        st.error(f"Save Failed: {e}")
                
        with col2:
            if st.button("▶️ Execute Script", use_container_width=True):
                if not edited_code and not code_content:
                    st.warning("Workspace empty.")
                else:
                    with st.spinner("Compiling & Running..."):
                        import subprocess
                        import tempfile
                        
                        code_to_run = edited_code if edited_code else st.session_state.editor_code
                        if isinstance(code_to_run, dict):
                            code_to_run = str(code_to_run)
                        
                        exec_dir = PROJECT_ROOT / "generated_project"
                        exec_dir.mkdir(parents=True, exist_ok=True)
                        
                        req_path = exec_dir / "requirements.txt"
                        if req_path.exists():
                           subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", str(req_path)], cwd=str(exec_dir))
                        
                        filename = "run_temp.py"
                        if st.session_state.get('current_file') and not st.session_state.get('current_file').startswith("✨"):
                            filename = Path(st.session_state.current_file).name
                        elif hasattr(st.session_state, 'current_file') and "✨ Generated: " in st.session_state.current_file:
                            filename = st.session_state.current_file.replace("✨ Generated: ", "")
                            
                        tmp_path = exec_dir / f"tmp_{filename}"
                        
                        try:
                            tmp_path.parent.mkdir(parents=True, exist_ok=True)
                            tmp_path.write_text(code_to_run, encoding="utf-8")
                            
                            if tmp_path.suffix != ".py":
                                st.session_state.terminal_output = f"Warning: {filename} is a non-Python component and lacks a direct execution context."
                                st.session_state.terminal_error = ""
                                st.session_state.exec_time = "0.0s"
                                st.session_state.exit_code = 0
                            else:
                                env = os.environ.copy()
                                env["PYTHONPATH"] = str(exec_dir)
                                
                                start_time = time.time()
                                result = subprocess.run(
                                    [sys.executable, str(tmp_path)],
                                    capture_output=True,
                                    text=True,
                                    timeout=30,
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
                           st.session_state.terminal_error = f"Runtime Crash: {e}"
                           st.session_state.exec_time = "N/A"
                           st.session_state.exit_code = -1
                        finally:
                            try:
                                if tmp_path.exists():
                                    tmp_path.unlink()
                            except:
                                pass
                                
        with col3:
            if st.button("🐳 Build Docker Image", use_container_width=True):
                try:
                    result1 = generate_requirements("generated_project", "fastapi")
                    result2 = generate_dockerfile("generated_project", "fastapi")
                    st.toast(result1, icon="🐳")
                    st.toast(result2, icon="🐳")
                except Exception as e:
                    st.error(f"Build Failed: {e}")

        with col4:
            if st.button("🚀 Commit to GitHub", use_container_width=True):
                result = push_to_github("generated_project", "autodevcrew-demo-build")
                if "Error" in result:
                     st.error(result)
                else:
                     st.toast("Pushed remote branch successfully!", icon="🐙")

        # ---------- Terminal Emulation ----------
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 🖥️ Native Output Console")
        st.caption("Standard Output (STDOUT) and Standard Error (STDERR) streams.")
        
        term_out = st.session_state.get("terminal_output", "")
        term_err = st.session_state.get("terminal_error", "")
        exec_time = st.session_state.get("exec_time", "")
        exit_code = st.session_state.get("exit_code", None)
        
        # Display runtime metrics
        if exit_code is not None:
            if exit_code == 0:
                st.success(f"Engine Detached • Time: {exec_time} • Status: 0 (OK)")
            else:
                st.error(f"Engine Crash • Time: {exec_time} • Status: {exit_code} (FAIL)")
                
        # Consolidated pseudo-terminal wrapper
        terminal_wrap = f"""
```bash
# user@autodevcrew:~/workspace/generated_project$ python script.py
"""
        if not term_out and not term_err:
            terminal_wrap += "\n[No stdout or stderr output recorded]"
        if term_out:
            terminal_wrap += f"\n{term_out}"
        if term_err:
            terminal_wrap += f"\n[stderr]\n{term_err}"
            
        terminal_wrap += "\n```"
        st.markdown(terminal_wrap)

    else:
        st.info("⬅️ Initialize your environment by selecting a source file from the project directory.")

if __name__ == "__main__":
    render_editor()
