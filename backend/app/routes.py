# File: backend/app/routes.py

from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
import os
import logging

from .schemas import UploadResponse, Table, TableRow
from .utils import (
    extract_text_from_pdf, 
    extract_text_from_docx, 
    extract_text_from_txt, 
    compute_metrics, 
    extract_entities_with_spacy,
    chunk_text,
    batch_chunk_text
)

from typing import Dict, List

# Initialize logger
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

router = APIRouter()

@router.post("/api/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Handles the file upload, extracts text, tables, chunks the text,
    extracts entities, computes metrics, and returns the response.

    Supports .txt, .pdf, and .docx file formats.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        UploadResponse: Contains the metrics, list of chunks, extracted entities, and tables.
    """
    logger.info(f"Received file: {file.filename}")

    # Validate file type
    if not (file.filename.endswith('.pdf') or file.filename.endswith('.txt') or file.filename.endswith('.docx')):
        logger.error("Unsupported file type")
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a .txt, .pdf, or .docx file.")

    # Determine file type
    if file.filename.endswith('.pdf'):
        file_type = 'pdf'
    elif file.filename.endswith('.docx'):
        file_type = 'docx'
    else:
        file_type = 'txt'

    # Save the uploaded file temporarily
    temp_dir = "/tmp"
    temp_file_path = os.path.join(temp_dir, f"temp_{file.filename}")
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"Saved temporary file at: {temp_file_path}")

        # Extract text and tables based on file type
        if file_type == 'pdf':
            extracted_text, extracted_tables = extract_text_from_pdf(temp_file_path)
        elif file_type == 'docx':
            extracted_text, extracted_tables = extract_text_from_docx(temp_file_path)
        else:  # .txt
            extracted_text, extracted_tables = extract_text_from_txt(temp_file_path)

        if not extracted_text.strip() and not extracted_tables:
            logger.error("No text or tables found in the document")
            raise HTTPException(status_code=400, detail="No text or tables found in the document.")

        logger.info("Computing metrics before chunking...")
        # Compute metrics before chunking (optional if metrics_before are needed)
        metrics_before = compute_metrics(extracted_text, chunks=[])

        logger.info("Chunking text using Text Chunker...")
        # Chunk the text using text_chunker
        chunks_text_chunker = chunk_text(extracted_text, method='spacy')  # Adjust 'method' as needed
        logger.info(f"Total chunks created by text_chunker: {len(chunks_text_chunker)}")

        logger.info("Chunking text using Batch Chunker...")
        # Chunk the text using batch_chunker
        chunks_batch_chunker = batch_chunk_text(extracted_text, batch_size=500)  # Example batch size
        logger.info(f"Total chunks created by batch_chunker: {len(chunks_batch_chunker)}")

        # Compute metrics for each chunking method
        metrics_text_chunker = compute_metrics(extracted_text, chunks_text_chunker)
        metrics_batch_chunker = compute_metrics(extracted_text, chunks_batch_chunker)

        # Combine chunking results with their respective metrics
        chunking_results = {
            "text_chunker": chunks_text_chunker,
            "batch_chunker": chunks_batch_chunker
        }

        # Extract entities using different methods
        # Currently, only spaCy is implemented
        entities_spacy = extract_entities_with_spacy(extracted_text)
        entities_results = {
            "spacy": entities_spacy
            # Add other entity extractors here if available
        }

        logger.info("Computing metrics after chunking...")
        # Compute metrics after chunking (using text_chunker and batch_chunker)
        # Already computed above

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.info(f"Deleted temporary file at: {temp_file_path}")

    # Prepare the tables data
    tables_response = {}
    for extractor, tables in extracted_tables.items():
        extractor_tables = []
        for table in tables:
            table_rows = []
            for row in table.get("rows", []):
                # Ensure all cells are strings, replace None with empty string
                sanitized_cells = [cell if cell is not None else "" for cell in row.get("cells", [])]
                # Optionally, filter out rows where all cells are empty
                if any(cell.strip() for cell in sanitized_cells):
                    table_rows.append(TableRow(cells=sanitized_cells))
                else:
                    logger.debug("Skipping empty row.")
            # Only include tables that have at least one non-empty row
            if table_rows:
                # Ensure 'page_number' is an integer
                page_number = table.get("page_number", 0)
                if not isinstance(page_number, int):
                    logger.warning(f"Table {table.get('table_number',0)} has invalid page_number: {page_number}. Setting to 0.")
                    page_number = 0
                extractor_tables.append(Table(
                    page_number=page_number,
                    table_number=table.get("table_number", 0),
                    rows=table_rows
                ))
        if extractor_tables:
            tables_response[extractor] = extractor_tables

    # Prepare the response data
    response_data = {
        # Metrics can be structured per chunking method if needed
        "num_lines": metrics_text_chunker["num_lines"],
        "num_paragraphs": metrics_text_chunker["num_paragraphs"],
        "num_words": metrics_text_chunker["num_words"],
        "avg_words_per_paragraph": metrics_text_chunker["avg_words_per_paragraph"],
        "avg_words_per_line": metrics_text_chunker["avg_words_per_line"],
        "original_content_size": metrics_text_chunker["original_content_size"],
        "num_chunks": metrics_text_chunker["num_chunks"],
        "chunking": chunking_results,
        "entities": entities_results,  # Added entities to response
        "tables": tables_response  # Added tables to response
    }

    logger.info("Returning response with chunks, entities, and tables.")
    return UploadResponse(**response_data)
