# src/multimodal_llm/llm.py

import base64
from src.retrieval.retriever import retrieve_documents
from src.embedding.embedder import Embedder
from src.vector_db.vectordb import VectorDB
from langchain.chat_models import ChatOpenAI  # Updated import based on LangChain version
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize components
llm = ChatOpenAI(
    model_name='gpt-4',  # Verify if 'gpt-4o' was a typo; corrected to 'gpt-4'
    temperature=0,
    openai_api_key=Config.OPENAI_API_KEY
)
vector_db = VectorDB(Config.REDIS_URL, Config.CHROMA_COLLECTION_NAME)
embedder = Embedder()

def generate_response(query: str) -> dict:
    """
    Generate a response for the given query using the RAG pipeline.

    Args:
        query (str): The user's query.

    Returns:
        dict: A dictionary containing the answer and sources.
    """
    try:
        logger.info("Starting RAG pipeline...")

        # Step 1: Retrieve relevant documents
        documents = retrieve_documents(query, vector_db)

        if not documents:
            logger.warning("No documents retrieved from VectorDB.")

        # Step 2: Process documents (e.g., handle images if any)
        processed_docs = []
        for doc in documents:
            doc_texts = doc.get('texts', [])
            doc_images = doc.get('images', [])
            # Encode images to base64 if they exist
            encoded_images = [base64.b64encode(image).decode('utf-8') for image in doc_images]
            processed_docs.append({
                "texts": doc_texts,
                "images": encoded_images
            })

        # Step 3: Build prompt
        prompt = build_prompt(query, processed_docs)

        # Step 4: Generate answer using LLM
        try:
            answer_response = llm.invoke(prompt)  # Use 'invoke' instead of '__call__'
            if hasattr(answer_response, 'content'):
                answer = answer_response.content  # Extract string content from AIMessage
            elif isinstance(answer_response, str):
                answer = answer_response  # Directly assign if it's already a string
            else:
                logger.error("Unexpected response type from LLM.")
                raise ValueError("LLM returned an unexpected response type.")
        except AttributeError as attr_err:
            logger.error(f"Attribute error during LLM invocation: {attr_err}")
            raise
        except Exception as e:
            logger.error(f"Error invoking LLM: {e}")
            raise

        logger.info("RAG pipeline completed successfully.")

        # Prepare sources as a dictionary with 'texts' and 'images' keys
        sources_texts = []
        sources_images = []
        for doc in processed_docs:
            sources_texts.extend(doc.get("texts", []))
            sources_images.extend(doc.get("images", []))

        # Ensure that sources_texts and sources_images are lists
        sources = {
            "texts": sources_texts,
            "images": sources_images
        }

        return {
            "answer": answer,    # Should be a string
            "sources": sources   # Should be a dictionary with 'texts' and 'images'
        }

    except Exception as e:
        logger.error(f"Error in generate_response: {e}")
        raise e

def build_prompt(query: str, documents: list) -> str:
    """
    Build a prompt for the LLM using the query and retrieved documents.

    Args:
        query (str): The user's query.
        documents (list): Retrieved documents containing texts and images.

    Returns:
        str: The constructed prompt.
    """
    try:
        prompt = f"User Query: {query}\n\n"
        for doc in documents:
            if 'texts' in doc and doc['texts']:
                prompt += "Text:\n" + "\n".join(doc['texts']) + "\n\n"
            if 'images' in doc and doc['images']:
                for img in doc['images']:
                    prompt += f"Image: [base64]{img}[/base64]\n\n"
        prompt += "Provide a comprehensive answer based on the above information."
        return prompt
    except Exception as e:
        logger.error(f"Error in build_prompt: {e}")
        raise e
