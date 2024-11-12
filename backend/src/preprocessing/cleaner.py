# backend/src/preprocessing/cleaner.py

import re
import logging

logger = logging.getLogger(__name__)

def clean_data(raw_text: str) -> str:
    """
    Clean the extracted raw text.

    Args:
        raw_text (str): The raw extracted text.

    Returns:
        str: The cleaned text.
    """
    try:
        # Example cleaning: remove multiple spaces, non-printable characters
        cleaned = re.sub(r'\s+', ' ', raw_text)
        cleaned = re.sub(r'[^\x20-\x7E]+', '', cleaned)
        logger.info("Data cleaned successfully.")
        return cleaned
    except Exception as e:
        logger.error(f"Error cleaning data: {e}")
        raise e

def chunk_data(cleaned_text: str, max_chars: int = 500) -> list:
    """
    Split the cleaned text into chunks based on paragraph breaks and maximum characters.

    Args:
        cleaned_text (str): The cleaned text.
        max_chars (int, optional): Maximum number of characters per chunk. Defaults to 500.

    Returns:
        list: List of text chunks.
    """
    try:
        paragraphs = cleaned_text.split('\n\n')
        chunks = []
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) + 1 <= max_chars:
                current_chunk += " " + para if current_chunk else para
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para

        if current_chunk:
            chunks.append(current_chunk.strip())

        logger.info(f"Data chunked into {len(chunks)} chunks.")
        return chunks
    except Exception as e:
        logger.error(f"Error chunking data: {e}")
        raise e
