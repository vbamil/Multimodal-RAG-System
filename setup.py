# setup.py
from setuptools import setup, find_packages

setup(
    name='multimodal_rag_system',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # Add all dependencies from backend/requirements.txt
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-dotenv",
        "langchain",
        "langchain-openai",
        "langchain-chroma",
        "langchain-community",
        "langchain-experimental",
        "unstructured[all-docs]",
        "htmltabletomd",
        "openai",
        "redis",
        "chroma",
        "Pillow",
        "tesseract",
        "poppler-utils",
        "speechrecognition",
        "pydub",
        "beautifulsoup4",
    ],
)
