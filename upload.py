import os
from app import get_retriever, get_transcript_ans
from constants import *
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path


DB = None


# This function will create the directory if it does not exist
def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)


# Save files
def save_file(uploaded_files):
    ensure_dir(source_dir)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(source_dir, uploaded_file.name)

            # Write the uploaded PDF to a new file in the directory
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())


def clear_folder():
    folder = Path(source_dir)
    if folder.exists():
        for file in folder.iterdir():
            # Check if the file is a regular file (not a directory)
            if file.is_file():
                # Remove the file
                file.unlink()


def to_text():
    loader = DirectoryLoader(
        f"{source_dir}", glob="./*.docx", loader_cls=UnstructuredWordDocumentLoader
    )
    documents = loader.load()
    return documents


def get_doc_ans(query):
    return get_transcript_ans(DB, query)


def ingest_pdf(uploaded_files):
    clear_folder()
    save_file(uploaded_files)
    texts = to_text()
    get_retriever(texts)
    return
