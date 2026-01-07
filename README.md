# AutoDevCrew 🚀

AutoDevCrew is a complete intelligent DevOps multi-agent system. It orchestrates a team of AI agents (Engineer, Tester, DevOps, Summarizer) to autonomously act on software requirements.

## Features
- **Multi-Agent Architecture**: Specialized agents for coding, testing, and deployment.
- **Memory Management**: ChromaDB integration for persistent knowledge.
- **LLM Engine**: HuggingFace Transformers integration.
- **Interfaces**: Streamlit Dashboard and FastAPI Server.
- **Deployment**: Docker and Cloud-ready (Colab, HF Spaces).

## Structure
- `src/agents`: Agent implementations.
- `src/core`: Core logic (Orchestrator, Event Bus, Memory, LLM).
- `src/interface`: API and UI.
- `data/chromadb`: Vector store data.

## Configuration
### Local LLM (Default)
The project is configured to use `TinyLlama` (running on CPU) by default if you set `provider: "local"` in `config.yaml`.

### Gemini API (Recommended for better results)
To use Google's Gemini Pro:
1.  Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey).
2.  Open `config.yaml`.
3.  Set `provider: "gemini"`.
4.  Paste your key in `api_key: "YOUR_KEY_HERE"`.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run API Server
```bash
python src/main.py api
```

### Run Dashboard
```bash
python src/main.py dashboard
```

### Run CLI
```bash
python src/main.py cli --req "Create a binary search function"
```

## Deployment

### Docker
```bash
cd deployment
docker build -t autodevcrew .
docker run -p 8000:8000 -p 8501:8501 autodevcrew
```

## Contributing
Pull requests are welcome.
