# backend/src/embedding/embedder.py

import sys
import os

# Print sys.path for debugging inside embedder.py
print("sys.path inside embedder.py:")
for path in sys.path:
    print(f" - {path}")

from langchain_community.embeddings import OpenAIEmbeddings
from src.utils.config import Config  # Absolute import based on new structure
import logging

logger = logging.getLogger(__name__)

class Embedder:
    def __init__(self):
        """
        Initialize the Embedder with OpenAIEmbeddings.
        """
        try:
            print("Initializing OpenAIEmbeddings...")
            self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
            logger.info("OpenAIEmbeddings initialized successfully.")
            print("OpenAIEmbeddings initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing OpenAIEmbeddings: {e}")
            print(f"Error initializing OpenAIEmbeddings: {e}")
            raise e

    def generate_embeddings(self, chunks):
        """
        Generate embeddings for the given data chunks.

        Args:
            chunks (list): A list of data chunks.

        Returns:
            list: A list of embeddings.
        """
        try:
            logger.info("Generating embeddings for data chunks...")
            print(f"Generating embeddings for chunks: {chunks}")
            embeddings = self.embeddings.embed_documents(chunks)
            logger.info("Embeddings generated successfully.")
            print("Embeddings generated successfully.")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            print(f"Error generating embeddings: {e}")
            raise e

def generate_embeddings(chunks):
    """
    Convenience function to generate embeddings without instantiating the Embedder class.

    Args:
        chunks (list): A list of data chunks.

    Returns:
        list: A list of embeddings.
    """
    print("Calling generate_embeddings function.")
    embedder = Embedder()
    return embedder.generate_embeddings(chunks)
