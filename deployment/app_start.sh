#!/bin/bash
# Start API in background
python src/main.py api &

# Start Streamlit in foreground
streamlit run src/interface/dashboard_app.py --server.port 8501 --server.address 0.0.0.0
