import uvicorn
from fastapi import FastAPI
from uvicorn.config import LOGGING_CONFIG_DEFAULT_DICT

# Create a new FastAPI app
app = FastAPI(
    title="Attendance System",
    description="A simple attendance system",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    # Custom logging setup
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=LOGGING_CONFIG_DEFAULT_DICT,
        debug=False
    )

# Removed line that caused the parse error