# backend/app/populate_vector_db.py

import sys
import os
import logging

# Add project root to sys.path if not already added
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.data_extraction.extractor import extract_data
from src.preprocessing.cleaner import clean_data, chunk_data
from src.embedding.embedder import generate_embeddings
from src.vector_db.vectordb import VectorDB
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def populate_vector_db():
    try:
        # Step 1: Extract Data
        logger.info("Extracting data from source documents...")
        raw_data = extract_data("data/documents")  # Replace with your actual documents path

        # Step 2: Preprocess Data
        logger.info("Cleaning extracted data...")
        cleaned_data = clean_data(raw_data)

        # Step 3: Chunk Data
        logger.info("Chunking data into manageable segments...")
        chunks = chunk_data(cleaned_data)

        if not chunks:
            logger.warning("No data chunks generated. Aborting VectorDB population.")
            return

        # Step 4: Generate Embeddings
        logger.info("Generating embeddings for data chunks...")
        embeddings = generate_embeddings(chunks)

        if not embeddings:
            logger.warning("No embeddings generated. Aborting VectorDB population.")
            return

        # Step 5: Store in VectorDB
        logger.info("Initializing VectorDB...")
        vectordb = VectorDB(Config.REDIS_URL, Config.CHROMA_COLLECTION_NAME)
        logger.info("Adding documents to VectorDB...")
        vectordb.add_documents(embeddings, chunks)  # Ensure this method matches your VectorDB implementation

        logger.info("VectorDB population completed successfully.")

    except Exception as e:
        logger.error(f"Error populating VectorDB: {e}")
        raise e

if __name__ == "__main__":
    populate_vector_db()
