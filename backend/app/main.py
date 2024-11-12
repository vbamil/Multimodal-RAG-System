# File: backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .routes import router as upload_router

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG for detailed logs

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
ch.setFormatter(formatter)

# Add the handlers to the logger if not already added
if not logger.handlers:
    logger.addHandler(ch)

app = FastAPI(
    title="Multimodal RAG System Backend",
    description="API for uploading documents, extracting text, summarizing, and chunking.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Update as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the upload router
app.include_router(upload_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multimodal RAG System Backend!"}
