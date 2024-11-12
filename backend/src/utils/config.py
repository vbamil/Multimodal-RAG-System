# src/utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Config:
    # Paths
    PDF_PATH = os.getenv('PDF_PATH', './data/raw/IF10244.pdf')
    FIGURES_DIR = os.getenv('FIGURES_DIR', './data/figures')
    TEXT_CHUNKS_PATH = os.getenv('TEXT_CHUNKS_PATH', './data/processed/text_chunks.txt')
    TABLES_PATH = os.getenv('TABLES_PATH', './data/processed/tables.md')

    # OpenAI API
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Database Configurations
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    CHROMA_COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME', 'mm_rag')
