# backend/src/utils/summary.py

def generate_summary(text: str) -> dict:
    """
    Generate summary details of the document.

    Args:
        text (str): The cleaned text of the document.

    Returns:
        dict: A dictionary containing summary metrics.
    """
    lines = text.split('\n')
    paragraphs = [para for para in text.split('\n\n') if para.strip()]
    words = text.split()

    summary = {
        "number_of_lines": len(lines),
        "number_of_paragraphs": len(paragraphs),
        "number_of_words": len(words),
        "average_words_per_paragraph": round(len(words) / len(paragraphs), 2) if len(paragraphs) > 0 else 0,
        "average_words_per_line": round(len(words) / len(lines), 2) if len(lines) > 0 else 0
    }

    return summary
