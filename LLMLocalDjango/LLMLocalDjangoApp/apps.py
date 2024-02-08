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
        return super().ready()
