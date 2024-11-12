# File: backend/app/schemas.py

from typing import List, Dict
from pydantic import BaseModel

class TableRow(BaseModel):
    cells: List[str]

class Table(BaseModel):
    page_number: int
    table_number: int
    rows: List[TableRow]

class TablesExtractionResults(BaseModel):
    tables: List[Table]

class UploadResponse(BaseModel):
    # Metrics for the entire document
    num_lines: int
    num_paragraphs: int
    num_words: int
    avg_words_per_paragraph: float
    avg_words_per_line: float
    original_content_size: int
    num_chunks: int
    
    # Chunking results by method/library
    chunking: Dict[str, List[str]]  # e.g., {"text_chunker": [...], "batch_chunker": [...]}
    
    # Entity extraction results by method/library
    entities: Dict[str, List[List[dict]]]  # e.g., {"spaCy": [...], "AnotherNER": [...]}
    
    # Tables extracted by different methods/libraries
    tables: Dict[str, List[Table]]  # e.g., {"Camelot": [...], "pdfplumber": [...], "Tabula-py": [...]}
