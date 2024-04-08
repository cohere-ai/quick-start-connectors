import logging

import cohere
import pinecone

logger = logging.getLogger(__name__)

cohere_client = None
pinecone_client = None


class PineconeClient:
    def __init__(self, api_key, index):
        self.client = pinecone.Pinecone(api_key=api_key)
        self.index = self.client.Index(index)

    def query(self, query, top_k=100, include_metadata=True):
        return self.index.query(
            vector=query, top_k=top_k, include_metadata=include_metadata
        )


class CohereClient:
    def __init__(self, cohere_api_key):
        self.client = cohere.Client(cohere_api_key)

    def get_embeddings(self, query, model, input_type="search_query"):
        return self.client.embed([query], model=model, input_type=input_type).embeddings


def get_pinecone_client(api_key, index):
    global pinecone_client
    if not pinecone_client:
        pinecone_client = PineconeClient(api_key, index)

    return pinecone_client


def get_cohere_client(api_key):
    global cohere_client
    if not cohere_client:
        cohere_client = CohereClient(api_key)

    return cohere_client
