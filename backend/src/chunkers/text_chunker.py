# File: backend/src/chunkers/text_chunker.py

import re
from typing import List
import spacy
import nltk
import logging
import unicodedata

# Initialize SpaCy English model
try:
    nlp = spacy.load("en_core_web_lg")  # Upgraded to a larger model for better NER accuracy
except OSError:
    logging.info("Downloading 'en_core_web_lg' model...")
    from spacy.cli import download
    download("en_core_web_lg")
    nlp = spacy.load("en_core_web_lg")

# Download NLTK punkt tokenizer if not already downloaded
nltk.download('punkt', quiet=True)

from nltk.tokenize import sent_tokenize

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

# ----------------------------
# Text Cleaning Functions
# ----------------------------

def normalize_unicode(text: str) -> str:
    """
    Normalizes unicode characters to their closest ASCII representation.
    """
    logger.debug("Normalizing unicode characters...")
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    return text

def fix_special_cases(text: str) -> str:
    """
    Fixes special cases specific to the text.
    """
    logger.debug("Fixing special cases...")
    # Replace common ligatures
    ligatures = {
        'ﬁ': 'fi',
        'ﬂ': 'fl',
        'ﬃ': 'ffi',
        'ﬄ': 'ffl',
        'ﬅ': 'ft',
        'ﬆ': 'st',
        'ﬀ': 'ff',
    }
    for ligature, replacement in ligatures.items():
        text = text.replace(ligature, replacement)
    return text

def remove_line_breaks(text: str) -> str:
    """
    Removes unnecessary line breaks within sentences.
    """
    logger.debug("Removing line breaks within sentences...")
    # Replace line breaks within sentences with a space
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    return text

def fix_hyphenation_and_spaces(text: str) -> str:
    """
    Corrects hyphenation issues and inserts missing spaces around hyphens.
    """
    logger.debug("Fixing hyphenation and missing spaces...")
    # Remove hyphens at line breaks
    text = re.sub(r'-\s*\n\s*', '', text)
    # Add spaces around hyphens if missing
    text = re.sub(r'(?<!\s)([-–—])(?!\s)', r' \1 ', text)
    return text

def fix_missing_spaces(text: str) -> str:
    """
    Inserts missing spaces between words where needed.
    """
    logger.debug("Fixing missing spaces...")
    # Insert space between words that are concatenated
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
    # Insert space after punctuation if missing
    text = re.sub(r'([.,!?;:])(?=[^\s])', r'\1 ', text)
    return text

def insert_missing_spaces_in_compounds(text: str) -> str:
    """
    Inserts spaces in concatenated compound words.
    """
    logger.debug("Inserting missing spaces in compound words...")
    # Insert space before capital letters following lowercase letters
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Handle cases where a word is concatenated with a hyphen but no spaces
    text = re.sub(r'([a-zA-Z])-(?=[a-zA-Z])', r'\1 - ', text)
    return text

def correct_common_errors(text: str) -> str:
    """
    Corrects common errors in text extracted from PDFs.
    """
    logger.debug("Correcting common extraction errors...")
    # Fix missing spaces around numbers and units (e.g., '6-10' to '6–10')
    text = re.sub(r'(\d)(–|-)(\d)', r'\1–\3', text)
    return text

def standardize_hyphens_and_dashes(text: str) -> str:
    """
    Replaces various hyphen and dash characters with a standard hyphen.
    """
    logger.debug("Standardizing hyphens and dashes...")
    # Replace en-dash and em-dash with hyphen
    text = text.replace('–', '-').replace('—', '-')
    return text

def remove_encoding_artifacts(text: str) -> str:
    """
    Removes encoding artifacts and non-standard characters.
    """
    logger.debug("Removing encoding artifacts...")
    # Remove patterns like (cid:88)
    text = re.sub(r'\(cid:\d+\)', '', text)
    # Remove other non-standard characters (retain common punctuation)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

def correct_urls(text: str) -> str:
    """
    Corrects URLs that have been split by spaces.
    """
    logger.debug("Correcting URLs...")
    # Example pattern: https: //github.com/...
    text = re.sub(r'https?:\s*//', 'https://', text)
    return text

def normalize_whitespace(text: str) -> str:
    """
    Replaces multiple spaces with a single space and normalizes newlines.
    """
    logger.debug("Normalizing whitespace...")
    # Replace multiple spaces with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Normalize newlines
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return text.strip()

def clean_text(text: str) -> str:
    """
    Comprehensive text cleaning function.
    """
    logger.info("Starting text cleaning...")
    text = normalize_unicode(text)
    text = fix_special_cases(text)
    text = remove_line_breaks(text)
    text = fix_hyphenation_and_spaces(text)
    text = fix_missing_spaces(text)
    text = insert_missing_spaces_in_compounds(text)
    text = correct_common_errors(text)
    text = standardize_hyphens_and_dashes(text)
    text = remove_encoding_artifacts(text)
    text = correct_urls(text)    
    text = normalize_whitespace(text)
    return text

# ----------------------------
# Sentence Splitting Functions
# ----------------------------

def split_into_sentences_spacy(text: str) -> List[str]:
    """
    Splits text into sentences using SpaCy.
    """
    logger.debug("Splitting text into sentences using SpaCy...")
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]

def split_into_sentences_nltk(text: str) -> List[str]:
    """
    Splits text into sentences using NLTK's sentence tokenizer.
    """
    logger.debug("Splitting text into sentences using NLTK...")
    return sent_tokenize(text)

def split_into_sentences(text: str, method: str = 'spacy') -> List[str]:
    """
    Splits text into sentences using the specified method ('spacy' or 'nltk').
    """
    if method == 'spacy':
        return split_into_sentences_spacy(text)
    elif method == 'nltk':
        return split_into_sentences_nltk(text)
    else:
        raise ValueError("Unsupported sentence splitting method. Choose 'spacy' or 'nltk'.")

# ----------------------------
# Chunking Functions
# ----------------------------

def group_sentences_into_chunks(
    sentences: List[str],
    min_words: int = 300,
    max_words: int = 500,
    overlap_sentences: int = 2
) -> List[str]:
    """
    Groups sentences into chunks within specified word limits, maintaining sentence integrity.
    Introduces overlapping sentences to preserve context between chunks.
    """
    logger.info("Grouping sentences into chunks...")
    chunks = []
    current_chunk = []
    current_word_count = 0
    overlap_buffer = []

    for sentence in sentences:
        sentence_word_count = len(sentence.split())
        
        # Check if adding the sentence exceeds max_words
        if current_word_count + sentence_word_count > max_words:
            if current_word_count >= min_words:
                # Add current chunk to chunks
                chunks.append(' '.join(current_chunk))
                
                # Handle overlap: take the last 'overlap_sentences' sentences
                if overlap_sentences > 0:
                    overlap_buffer = current_chunk[-overlap_sentences:]
                    current_chunk = overlap_buffer.copy()
                    current_word_count = sum(len(s.split()) for s in current_chunk)
                else:
                    current_chunk = []
                    current_word_count = 0
            else:
                # If current chunk is too small, add the sentence anyway
                pass  # Continue adding sentences

        # Add the sentence to the current chunk
        current_chunk.append(sentence)
        current_word_count += sentence_word_count

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    logger.info(f"Total chunks created: {len(chunks)}")
    return chunks

def group_sentences_with_overlap(
    sentences: List[str],
    min_words: int = 300,
    max_words: int = 500,
    overlap_sentences: int = 2
) -> List[str]:
    """
    Groups sentences into chunks with overlapping context windows.
    """
    return group_sentences_into_chunks(
        sentences,
        min_words=min_words,
        max_words=max_words,
        overlap_sentences=overlap_sentences
    )

# ----------------------------
# Duplicate Removal
# ----------------------------

def remove_duplicates(chunks: List[str]) -> List[str]:
    """
    Removes duplicate chunks to prevent redundancy.
    """
    logger.info("Removing duplicate chunks...")
    unique_chunks = []
    seen = set()
    for chunk in chunks:
        # Create a unique key based on the first 100 characters
        chunk_key = chunk[:100].lower()
        if chunk_key not in seen:
            unique_chunks.append(chunk)
            seen.add(chunk_key)
    logger.info(f"Total unique chunks after deduplication: {len(unique_chunks)}")
    return unique_chunks

# ----------------------------
# Main Chunking Function
# ----------------------------

def chunk_text(text: str, method: str = 'spacy') -> List[str]:
    """
    Processes the input text and returns a list of high-quality chunks.
    
    Args:
        text (str): The input text.
        method (str, optional): Sentence splitting method ('spacy' or 'nltk'). Defaults to 'spacy'.
    
    Returns:
        List[str]: A list of text chunks.
    """
    try:
        logger.info("Starting text cleaning...")
        cleaned_text = clean_text(text)
        
        logger.info("Splitting text into sentences...")
        sentences = split_into_sentences(cleaned_text, method=method)
        logger.info(f"Total sentences extracted: {len(sentences)}")
        
        logger.info("Grouping sentences into chunks with overlapping context...")
        chunks = group_sentences_with_overlap(
            sentences,
            min_words=300,
            max_words=500,
            overlap_sentences=2
        )
        
        logger.info("Removing duplicate chunks...")
        chunks = remove_duplicates(chunks)
        
        logger.info("Chunking completed.")
        
        return chunks
    except Exception as e:
        logger.error(f"Error during chunk_text: {e}")
        raise
