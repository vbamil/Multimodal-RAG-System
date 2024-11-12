# backend/app/models.py

from pydantic import BaseModel
from typing import List

class ChunkResponse(BaseModel):
    original_content_size: int  # Number of paragraphs
    number_of_chunks: int
    chunks: List[str]
