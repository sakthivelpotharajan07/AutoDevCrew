import streamlit as st
import requests
import json
import time

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import local modules
from src.interface.editor_app import render_editor

st.set_page_config(
    page_title="AutoDevCrew Workspace", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def apply_custom_css():
    css_path = PROJECT_ROOT / "src" / "interface" / "assets" / "custom_style.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
apply_custom_css()

st.title("🚀 AutoDevCrew UI Dashboard")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🚀 Pipeline", "💻 Code Editor", "🧠 Memory Explorer", "⚙️ Settings"])

API_URL = "http://localhost:8000"

if page == "💻 Code Editor":
    render_editor()
    
elif page == "🚀 Pipeline":
    with st.container(border=True):
        st.markdown("## ⚙️ Project Configuration")
        
        col_name, col_spacer = st.columns([1, 1])
        with col_name:
            project_name = st.text_input("Project Name", placeholder="e.g. ChatApp_Demo")
            
        requirement = st.text_area("Describe Project Scope", height=120, placeholder="e.g. Build a fully functional real-time chat application with WebSockets...")
        
        start_btn = st.button("🚀 Start Pipeline", use_container_width=True)
    
    if start_btn:
        if not requirement:
            st.error("⚠️ Please describe the project scope.")
        else:
            status_container = st.empty()
            status_container.info("🚀 Pipeline initializing...")
            
            try:
                # Start pipeline (returns immediately now due to BackgroundTasks)
                response = requests.post(f"{API_URL}/run_pipeline", json={"requirement": requirement}, timeout=10)
                
                if response.status_code == 200:
                    status_container.info("🔄 Pipeline started! Waiting for status...")
                    
                    # Poll the API for real-time status updates
                    data = {}
                    while True:
                        try:
                            status_resp = requests.get(f"{API_URL}/pipeline_status", timeout=5)
                            if status_resp.status_code == 200:
                                data = status_resp.json()
                                current_step = data.get("current_step", "Working...")
                                current_status = data.get("status", "RUNNING")
                                
                                if current_status == "IDLE":
                                    status_container.info(f"⏳ **Status**: {current_status} | **Step**: {current_step}")
                                elif current_status == "RUNNING":
                                    status_container.info(f"🤖 **Active Agent**: {current_step} - *Working on task...*")
                                elif current_status in ["SUCCESS", "FAILED"]:
                                    break
                        except Exception:
                            pass # Retry silently if polling fails
                        
                        time.sleep(1)

                    # Finished polling
                    status_container.empty()
                    st.markdown("---")
                    
                    # Fetching final details
                    final_context = data.get('context', {})
                    final_errors = data.get('errors', 'Unknown error')
                    
                    if data.get('status') == 'FAILED':
                        st.error(f"❌ Pipeline Failed: {final_errors}")
                        st.toast("❌ Pipeline Failed!", icon="❌")
                    else:
                        st.success(f"✅ Pipeline Successfully Completed!")
                        st.toast("🎉 Pipeline Successfully Completed! Check out your new project.", icon="🎉")
                    
                    live_url = final_context.get('live_url')
                    
                    tab1, tab2, tab3 = st.tabs(["🌐 Live Application preview", "💻 Generated Code", "🧪 Automated Tests"])
                    
                    with tab1:
                        if live_url:
                            st.markdown(f"#### Application running securely via Ngrok")
                            st.markdown(f"**Public URL:** [{live_url}]({live_url})")
                            import streamlit.components.v1 as components
                            components.iframe(live_url, height=650)
                        else:
                            st.info("No live URL was returned for this build.")
                            
                    with tab2:
                        st.subheader("Source Code Repository")
                        gen_code = final_context.get('generated_code', 'No code')
                        st.session_state.generated_code = gen_code  # Store for Editor
                        
                        if isinstance(gen_code, dict):
                            for filepath, content in gen_code.items():
                                with st.expander(f"📄 {filepath}", expanded=True):
                                    st.code(content, language="python" if filepath.endswith(".py") else ("html" if filepath.endswith(".html") else "javascript"))
                        else:
                            st.code(gen_code)
                            
                    with tab3:
                        st.subheader("Execution Testing")
                        st.code(final_context.get('tests', 'No tests'))
                        
                    st.info("💡 You can actively edit, execute, and version control this code directly in the **Code Editor** tab.")
                else:
                    st.error(f"🛑 Server Error: {response.text}")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out connecting to the backend API.")
            except Exception as e:
                st.error(f"🔌 Connection Failed: {e}. Make sure the `api` server is running.")

elif page == "🧠 Memory Explorer":
    st.header("🧠 Search Knowledge Base")
    with st.container():
        query = st.text_input("Semantic Search Query:", placeholder="e.g. Show me how user authentication was implemented before...")
        search_btn = st.button("🔍 Search Memory Database", use_container_width=True)
        
    if search_btn:
        with st.spinner("Scanning Semantic Vector Database..."):
            try:
                response = requests.get(f"{API_URL}/memory/search", params={"q": query}, timeout=10)
                if response.status_code == 200:
                    results = response.json()
                    documents = results.get('documents', [[]])[0]
                    metadatas = results.get('metadatas', [[]])[0]
                    distances = results.get('distances', [[]])[0]
                    ids = results.get('ids', [[]])[0]
                    
                    if not documents:
                        st.warning("No relevant memories found.")
                    else:
                        st.markdown("### 📊 Search Results")
                        for i, doc in enumerate(documents):
                            distance = distances[i] if len(distances) > i else 0
                            meta = metadatas[i] if len(metadatas) > i else {}
                            score = max(0, 1 - distance)
                            
                            with st.expander(f"📍 Match {i+1} • {meta.get('source', 'Unknown')} • Confidence: {score:.1%}", expanded=(i==0)):
                                st.markdown(f"**Context Type:** `{meta.get('type', 'Unknown')}`")
                                st.code(doc, language='python')
                                st.caption(f"Entry ID: {ids[i]}")

                else:
                    st.error("Search API failed.")
            except Exception as e:
                st.error(f"Connection Error: {e}")

elif page == "⚙️ Settings":
    st.header("⚙️ System Control & Settings")
    st.info("System configuration successfully loaded from core yaml profiles.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Environment Profiles**
        - Framework: FastAPI + Uvicorn
        - DB Context: SQLite Default mapping
        - Vector DB: ChromaDB
        """)
    with col2:
        st.markdown("""
        **Pipeline Variables**
        - Artifact Root: `generated_project/`
        - Exposed Port: `8080` (External)
        - Ngrok Tunnel: Active
        """)
