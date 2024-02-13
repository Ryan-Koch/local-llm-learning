import configparser
import os

from langchain_community.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_experimental.text_splitter import SemanticChunker


from LLMLocalDjangoApp import vector_store

global_config = configparser.ConfigParser()
global_config.read("global_settings.local")

base_url = global_config.get("global_settings", "base_url")

gdoc_config = configparser.ConfigParser()
gdoc_config.read("gdoc_settings.local")

folder_id = gdoc_config.get("gdoc_settings", "folder_id")
credential_path = gdoc_config.get("gdoc_settings", "credential_path")


def main():
    # This looks like it shouldn't be needed. But it is, even if the value isn't important. More in this GH issue: https://github.com/langchain-ai/langchain/issues/14725.
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""

    print("Loading Google Drive documents...")
    loader = GoogleDriveLoader(
        folder_id=folder_id,
        credentials_path=credential_path,
        token_path="./token.json",
        file_types=[
            "document",
        ],
        recursive=False,
    )
    # Get all the stuff in the gdocs folder
    data = loader.load()

    # Splitting the docs up
    print("Splitting documents...")
    text_splitter = SemanticChunker(OllamaEmbeddings(base_url=base_url, model="llama2"))
    # Okay, so if you don't do this locally you will get an index error when this runs: https://github.com/langchain-ai/langchain/compare/master...psaegert:langchain:master
    # hopefully this or something similar will appear in a PR on the library repo soon.
    documents = text_splitter.split_documents(data)

    # Initialize the vector store
    print("Initializing vector store...")
    vs = vector_store.VectorStore()
    vs.create_store(documents, OllamaEmbeddings(base_url=base_url, model="llama2"))

    print("Done!")
    return True


if __name__ == "__main__":
    main()
