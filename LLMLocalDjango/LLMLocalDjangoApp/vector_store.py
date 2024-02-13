import configparser

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


# This is hear so we can generate a store during application start up and then use it other places.
class VectorStore:
    vector_store = None

    # Used in apps.py to create the store.
    def create_store(self, all_splits, oembed):
        base_url = self.get_base_url()

        oembed = OllamaEmbeddings(base_url=base_url, model="llama2")
        VectorStore.vector_store = Chroma.from_documents(
            all_splits, oembed, persist_directory="./vector_store"
        )

    # Used to retrieve the created store.
    def get_store(self):
        return VectorStore.vector_store

    def initialize_store(self):
        base_url = self.get_base_url()
        oembed = OllamaEmbeddings(base_url=base_url, model="llama2")

        VectorStore.vector_store = Chroma(
            persist_directory="./vector_store", embedding_function=oembed
        )
        return VectorStore.vector_store

    def get_base_url(self):
        global_config = configparser.ConfigParser()
        global_config.read("global_settings.local")
        return global_config.get("global_settings", "base_url")
