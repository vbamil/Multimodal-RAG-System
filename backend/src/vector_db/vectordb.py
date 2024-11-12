# backend/src/vector_db/vectordb.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from src.utils.config import Config
import logging

logger = logging.getLogger(__name__)

class VectorDB:
    def __init__(self, redis_url: str, collection_name: str, persist_directory: str = './chroma_db'):
        """
        Initialize the VectorDB with Chroma.

        Args:
            redis_url (str): Redis connection URL.
            collection_name (str): Name of the Chroma collection.
            persist_directory (str): Directory to persist the Chroma database.
        """
        try:
            self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
            self.vector_store = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=persist_directory
            )
            logger.info(f"VectorDB initialized with collection: {collection_name}")
        except Exception as e:
            logger.error(f"Error initializing VectorDB: {e}")
            raise e

    def add_documents(self, embeddings: list, documents: list):
        """
        Add documents and their embeddings to the vector database.

        Args:
            embeddings (list): A list of embeddings.
            documents (list): A list of documents corresponding to the embeddings.
        """
        try:
            logger.info("Adding documents to VectorDB...")
            self.vector_store.add_texts(texts=documents, embeddings=embeddings)
            # Since manual persistence is deprecated, no need to call persist()
            logger.info("Documents added to VectorDB successfully.")
        except Exception as e:
            logger.error(f"Error adding documents to VectorDB: {e}")
            raise e

    def similarity_search(self, query: str, k: int = 5):
        """
        Query the vector database for relevant documents.

        Args:
            query (str): The query string.
            k (int): Number of top similar documents to retrieve.

        Returns:
            list: A list of relevant documents.
        """
        try:
            logger.info(f"Performing similarity search for query: {query}")
            results = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Retrieved {len(results)} documents from VectorDB.")
            return results
        except Exception as e:
            logger.error(f"Error during similarity search: {e}")
            raise e
