# Multimodal RAG System

## Overview
The Multimodal RAG System is a comprehensive application designed to facilitate Retrieval-Augmented Generation (RAG) using Large Language Models (LLMs). It enables users to upload documents, extract and process their content, store embeddings in a vector database, and interact with the system via a user-friendly frontend interface. The system supports summarization, entity extraction, and table extraction from various document formats.

## Features
- Document Upload: Supports .pdf, .docx, and .txt file formats.
- Text Extraction: Extracts and processes text from uploaded documents.
- Chunking: Divides text into manageable chunks for efficient processing.
- Embedding: Generates embeddings using LLMs and stores them in Chroma DB.
- Summarization: Provides concise summaries of the uploaded content.
- Entity and Table Extraction: Extracts entities and tables from documents.
- User Interface: Interactive frontend built with React for a seamless user experience.
- Caching: Implements caching mechanisms to optimize performance.
- Logging: Comprehensive logging for monitoring and debugging.
- Testing: Includes tests for various components to ensure reliability.

## Technologies Used

Backend
- Python 3.12
- FastAPI: Web framework for building APIs.
- Uvicorn: ASGI server for running FastAPI applications.
- AIocache: Asynchronous caching library.
- Transformers: Hugging Face library for LLMs.
- Chroma DB: Vector database for storing embeddings.
- SpaCy: NLP library for entity extraction.
- PDFPlumber & Docx: Libraries for document text extraction.
- NLTK: Natural Language Toolkit for text processing.

Frontend
- React.js
- JavaScript/TypeScript
- CSS

Others
- Docker: For containerization (if applicable).
- Git: Version control.
- Jupyter Notebooks: For data processing and experimentation.

### Folder Structure

multimodal-rag-system/
├── backend/
│   ├── app/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── download_nltk.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── populate_vector_db.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── utils.py
│   ├── chroma_db/
│   ├── src/
│   ├── tests/
│   ├── venv/
│   ├── requirements.txt
├── chroma_db/
│   ├── 442d9bf3-896f-478d-95e8-1bae834e3d96/
│   └── chroma.sqlite3
├── data/
│   ├── chunks/
│   ├── documents/
│   ├── processed/
│   ├── raw/
│   └── README.md
├── frontend/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── AnswerDisplay.js
│   │   │   ├── ChunkingDetails.css
│   │   │   ├── ChunkingDetails.js
│   │   │   ├── ChunksView.css
│   │   │   ├── ChunksView.js
│   │   │   ├── EntitiesView.css
│   │   │   ├── EntitiesView.js
│   │   │   ├── MetricsSummary.css
│   │   │   ├── MetricsSummary.js
│   │   │   ├── NavigationButtons.js
│   │   │   ├── QueryInput.js
│   │   │   ├── TablesView.css
│   │   │   ├── TablesView.js
│   │   │   ├── UploadForm.css
│   │   │   └── UploadForm.js
│   │   ├── pages/
│   │   │   ├── HomePage.css
│   │   │   └── HomePage.js
│   │   ├── __init__.py
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── App.test.js
│   │   ├── index.css
│   │   ├── index.js
│   │   ├── reportWebVitals.js
│   │   └── setupTests.js
│   ├── .env
│   ├── .gitignore
│   ├── package-lock.json
│   ├── package-lock.json.bak
│   ├── package.json
│   ├── package.json.bak
│   └── README.md
├── logs/
│   └── app.log
├── notebooks/
│   ├── 01_data_extraction.ipynb
│   ├── 02_chunking.ipynb
│   ├── 03_embedding.ipynb
│   ├── 04_vector_db.ipynb
│   ├── 05_retrieval.ipynb
│   └── 06_frontend_backend.ipynb
├── scripts/
│   └── setup.sh
├── tests/
│   ├── backend/
│   ├── chunkers/
│   ├── data_extraction/
│   ├── embedding/
│   ├── frontend/
│   ├── multimodal_llm/
│   ├── parsers/
│   ├── preprocessing/
│   ├── retrieval/
│   ├── utils/
│   └── vector_db/
├── venv/
│   ├── bin/
│   ├── include/
│   ├── lib/
│   ├── share/
│   └── pyvenv.cfg
├── .env
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py

### Installation
Prerequisites
Python 3.12
Node.js (for frontend)
Git
Virtual Environment Tool (e.g., venv, virtualenv)
Hugging Face Token (if accessing private models)
Backend Setup

Clone the Repository:

git clone https://github.com/yourusername/multimodal-rag-system.git
cd multimodal-rag-system/backend

Create and Activate Virtual Environment:

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies:

pip install -r requirements.txt
Configure Environment Variables:

Create a .env file in the backend directory with the following variables:

LLAMA_MODEL_PATH=meta-llama/Llama-3.2-1B
HUGGINGFACE_TOKEN=your_huggingface_token_here
Replace your_huggingface_token_here with your actual Hugging Face token.

Download NLTK Data:

Run the download_nltk.py script to download necessary NLTK data.

python app/download_nltk.py
Frontend Setup
Navigate to Frontend Directory:

cd ../frontend
Install Node Dependencies:

npm install
Configure Environment Variables:

Create a .env file in the frontend directory with necessary variables (e.g., API endpoints).

REACT_APP_API_URL=http://localhost:8000
Running the Application
Backend
Start the FastAPI Server:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
The backend API will be accessible at http://localhost:8000.

Frontend
Start the React App:

In a new terminal window/tab:

cd /path/to/multimodal-rag-system/frontend
npm start
The frontend will be accessible at http://localhost:3000.

### Usage
Access the Frontend Interface:

Open your browser and navigate to http://localhost:3000.

#### Upload a Document:

Click on the upload form to select a .pdf, .docx, or .txt file.
Submit the file to initiate processing.
View Metrics and Summary:

After processing, view the extracted metrics (word count, character count, sentences, paragraphs).
Read the generated summary of the document.
Interact with Extracted Data:

View entities extracted from the document.
Explore tables extracted from the document.
Running Tests
Backend Tests
Navigate to Backend Directory:

cd /path/to/multimodal-rag-system/backend
Run Tests:

pytest tests/
Frontend Tests
Navigate to Frontend Directory:

cd /path/to/multimodal-rag-system/frontend
Run Tests:

npm test
Contributing
Contributions are welcome! Please follow these steps:

Fork the Repository

Create a New Branch:


git checkout -b feature/YourFeatureName
Commit Your Changes:

git commit -m "Add Your Feature"
Push to the Branch:


git push origin feature/YourFeatureName
Open a Pull Request

Please ensure that your code adheres to the project's coding standards and passes all tests.



## Additional Notes
Chroma DB: Ensure that the chroma_db directory is correctly set up and accessible by the backend. This directory stores the vector embeddings generated by the system.

Data Directory: The data directory contains various subdirectories for raw, processed, and chunked documents. Ensure proper permissions and data management practices are followed.

Notebooks: The notebooks directory contains Jupyter notebooks for different stages of data processing, embedding, and retrieval. These are useful for experimentation and understanding the data flow.

Scripts: The scripts directory includes setup scripts like setup.sh. Ensure these scripts have the necessary execute permissions and are up-to-date.

Testing: Comprehensive tests are located in the tests directory, categorized by functionality. Regularly run tests to ensure system reliability.

Environment Variables: Both backend and frontend have their own .env files. Ensure that sensitive information like API keys and tokens are securely stored and not committed to version control.

Logging: Logs are stored in the logs directory. Monitor app.log for any runtime issues or errors.

By following the instructions in this README, you should be able to set up, run, and contribute to the Multimodal RAG System effectively. If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

Happy coding!
