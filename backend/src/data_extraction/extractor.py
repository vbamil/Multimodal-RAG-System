# backend/src/data_extraction/extractor.py

from fastapi import UploadFile
import PyPDF2
import io
import logging

logger = logging.getLogger(__name__)

async def extract_data_from_file(file: UploadFile) -> str:
    """
    Extract text data from an uploaded file.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        str: Extracted text.
    """
    try:
        if file.content_type == "text/plain":
            data = await file.read()
            text = data.decode('utf-8')
            logger.info(f"Extracted text from plain text file: {file.filename}")
            return text
        elif file.content_type == "application/pdf":
            data = await file.read()
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(data))
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            logger.info(f"Extracted text from PDF file: {file.filename}")
            return text
        else:
            logger.warning(f"Unsupported file type: {file.content_type}")
            raise ValueError(f"Unsupported file type: {file.content_type}")
    except Exception as e:
        logger.error(f"Error extracting data from file {file.filename}: {e}")
        raise e
