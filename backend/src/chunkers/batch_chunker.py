# File: backend/src/chunkers/batch_chunker.py

import os
from typing import List
from .text_chunker import chunk_text  # Ensure correct import path
import logging

# Configure logging
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

def batch_process_documents(input_dir: str, output_dir: str, method: str = 'spacy'):
    """
    Processes all text documents in the input directory and saves their chunks to the output directory.
    
    Args:
        input_dir (str): Directory containing input text documents.
        output_dir (str): Directory to save the output chunks.
        method (str, optional): Sentence splitting method ('spacy' or 'nltk'). Defaults to 'spacy'.
    """
    logger.info(f"Starting batch processing of documents in {input_dir}")
    
    # List all .txt files in the input directory
    documents = [doc for doc in os.listdir(input_dir) if doc.endswith('.txt')]
    
    if not documents:
        logger.warning("No text documents found in the input directory.")
        return
    
    for doc in documents:
        doc_path = os.path.join(input_dir, doc)
        doc_output_dir = os.path.join(output_dir, os.path.splitext(doc)[0])
        logger.info(f"Processing document: {doc_path}")
        
        # Ensure output directory exists
        os.makedirs(doc_output_dir, exist_ok=True)
        
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Chunk the text
            chunks = chunk_text(text, method=method)
            logger.info(f"Total chunks created for {doc}: {len(chunks)}")
            
            # Save chunks to individual text files
            for idx, chunk in enumerate(chunks, 1):
                chunk_filename = f"chunk_{idx}.txt"
                chunk_path = os.path.join(doc_output_dir, chunk_filename)
                with open(chunk_path, 'w', encoding='utf-8') as cf:
                    cf.write(chunk)
                logger.debug(f"Saved chunk {idx} to {chunk_path}")
        
        except Exception as e:
            logger.error(f"Failed to process document {doc}: {e}")
    
    logger.info("Batch processing completed successfully.")

def batch_chunk_text(text: str, batch_size: int = 500) -> List[str]:
    """
    Chunk text into batches of a specified size.
    
    Args:
        text (str): The input text.
        batch_size (int, optional): Number of words per chunk. Defaults to 500.
    
    Returns:
        List[str]: List of text chunks.
    """
    logger.info(f"Batch chunking text into chunks of {batch_size} words.")
    words = text.split()
    chunks = [' '.join(words[i:i + batch_size]) for i in range(0, len(words), batch_size)]
    logger.debug(f"Batch chunker produced {len(chunks)} chunks.")
    return chunks

if __name__ == "__main__":
    # Example usage
    input_directory = "/path/to/input/documents/"  # Replace with your documents directory
    output_directory = "/path/to/output/chunks/"  # Replace with your desired output directory
    chunking_method = 'spacy'  # or 'nltk'
    
    batch_process_documents(input_directory, output_directory, method=chunking_method)
