# src/retrieval/retriever.py

import logging

logger = logging.getLogger(__name__)

def retrieve_documents(query, vector_db, k=5):
    """
    Retrieve relevant documents from the vector database based on the query.

    Args:
        query (str): The user's query.
        vector_db (VectorDB): An instance of the VectorDB class.
        k (int): Number of top similar documents to retrieve.

    Returns:
        list: A list of relevant documents.
    """
    try:
        logger.info(f"Retrieving documents for query: {query}")
        results = vector_db.similarity_search(query, k=k)
        documents = []
        for doc in results:
            # Assuming each doc has 'page_content' and 'metadata'
            documents.append({
                "texts": [doc.page_content],
                "images": []  # Extend this if handling images
            })
        logger.info(f"Retrieved {len(documents)} documents for the query.")
        return documents
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        raise e
