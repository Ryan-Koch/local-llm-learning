from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma


# This is hear so we can generate a store during application start up and then use it other places.
class VectorStore:
    vector_store = None

    # Used in apps.py to create the store.
    def create_store(self, all_splits, oembed):
        oembed = OllamaEmbeddings(base_url="http://localhost:11434", model="llama2")
        VectorStore.vector_store = Chroma.from_documents(all_splits, oembed)

    # Used to retrieve the created store.
    def get_store(self):
        return VectorStore.vector_store
