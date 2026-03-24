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

st.set_page_config(page_title="AutoDevCrew Dashboard", layout="wide")

st.title("🚀 AutoDevCrew Control Center")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Pipeline", "Code Editor", "Memory Explorer", "Settings"])

API_URL = "http://localhost:8000"

if page == "Code Editor":
    render_editor()
    
elif page == "Pipeline":
    st.header("Run Development Pipeline")
    requirement = st.text_area("Enter Requirement:", height=150)
    
    if st.button("Start Pipeline"):
        if not requirement:
            st.error("Please enter a requirement.")
        else:
            with st.spinner("Running Agents..."):
                try:
                    # Set a long timeout (e.g., 600 seconds = 10 minutes)
                    response = requests.post(f"{API_URL}/run_pipeline", json={"requirement": requirement}, timeout=600)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data['status'] == 'FAILED':
                             st.error(f"Pipeline Failed: {data.get('errors', 'Unknown error')}")
                        else:
                             st.success(f"Pipeline Finished: {data['status']}")
                        
                        st.subheader("Generated Code")
                        # Debug: show raw data if 'generated_code' is missing
                        if 'generated_code' not in data['context']:
                             st.warning("No code generated. Logic returned: " + str(data))
                        
                        live_url = data['context'].get('live_url')
                        if live_url:
                            st.write("---")
                            st.write("### 🌐 Live URL")
                            st.markdown(f"[{live_url}]({live_url})")
                            st.write("### 🚀 Running Application")
                            import streamlit.components.v1 as components
                            components.iframe(live_url, height=600)
                            st.write("---")
                        
                        gen_code = data['context'].get('generated_code', 'No code')
                        st.session_state.generated_code = gen_code  # Store for Editor
                        
                        if isinstance(gen_code, dict):
                            for filepath, content in gen_code.items():
                                st.write(f"**{filepath}**")
                                st.code(content, language="python")
                        else:
                            st.code(gen_code)
                        
                        st.subheader("Generated Tests")
                        st.code(data['context'].get('tests', 'No tests'))
                        st.success("Code available in 'Code Editor' tab!")
                    else:
                        st.error(f"Error: {response.text}")
                except requests.exceptions.Timeout:
                    st.error("Request timed out. The model might still be loading or generating. Check server logs.")
                except Exception as e:
                    st.error(f"Connection Failed: {e}. Make sure API server is running.")

elif page == "Memory Explorer":
    st.header("Search Knowledge Base")
    query = st.text_input("Search query:")
    if st.button("Search"):
        try:
            response = requests.get(f"{API_URL}/memory/search", params={"q": query}, timeout=10)
            if response.status_code == 200:
                results = response.json()
                
                # ChromaDB structure: {'ids': [[id1, id2]], 'documents': [[doc1, doc2]], 'metadatas': [[meta1, meta2]], 'distances': [[0.1, 0.2]]}
                documents = results.get('documents', [[]])[0]
                metadatas = results.get('metadatas', [[]])[0]
                distances = results.get('distances', [[]])[0]
                ids = results.get('ids', [[]])[0]
                
                if not documents:
                    st.info("No relevant memories found.")
                else:
                    for i, doc in enumerate(documents):
                        distance = distances[i] if len(distances) > i else 0
                        meta = metadatas[i] if len(metadatas) > i else {}
                        
                        # Approximate similarity score (1 - distance)
                        score = max(0, 1 - distance)
                        
                        with st.expander(f"Result {i+1} | Source: {meta.get('source', 'Unknown')} | Score: {score:.2f}"):
                            st.markdown(f"**Type:** `{meta.get('type', 'Unknown')}`")
                            st.code(doc, language='python') # Assuming code mostly
                            st.caption(f"ID: {ids[i]}")

            else:
                st.error("Search failed.")
        except Exception as e:
            st.error(f"Connection Error: {e}")

elif page == "Settings":
    st.header("System Settings")
    st.write("Configuration loaded from `config.yaml`.")
