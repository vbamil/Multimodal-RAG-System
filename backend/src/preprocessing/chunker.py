# backend/src/preprocessing/chunker.py

def chunk_data(text: str, max_paragraphs: int = 5) -> List[str]:
    """
    Split the text into chunks, each containing up to max_paragraphs.

    Args:
        text (str): The cleaned text of the document.
        max_paragraphs (int): Maximum number of paragraphs per chunk.

    Returns:
        List[str]: A list of text chunks.
    """
    paragraphs = [para for para in text.split('\n\n') if para.strip()]
    chunks = []
    current_chunk = []

    for paragraph in paragraphs:
        current_chunk.append(paragraph)
        if len(current_chunk) >= max_paragraphs:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []

    # Add any remaining paragraphs as the last chunk
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks
