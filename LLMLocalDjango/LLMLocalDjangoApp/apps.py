import glob
import os

from django.apps import AppConfig
from langchain.llms import Ollama
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from LLMLocalDjangoApp import vector_store


class LlmlocaldjangoappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "LLMLocalDjangoApp"

    def ready(self) -> None:
        ollama = Ollama(base_url="http://localhost:11434", model="llama2")

        # get all the PDFs in the documents folder
        directory = "./LLMLocalDjangoApp/static/LLMLocalDjangoApp/documents"
        pdf_paths = glob.glob(os.path.join(directory, "*.pdf"))

        # load the PDFs into the vector store
        for pdf_path in pdf_paths:
            data = UnstructuredPDFLoader(pdf_path).load()
            # splits up the documents into pieces to make search easier. Then we initiatlize the vector store with the pieces.
            splitter = RecursiveCharacterTextSplitter()
            all_splits = splitter.split_documents(data)
            vs = vector_store.VectorStore()
            vs.create_store(all_splits, ollama)

        return super().ready()
