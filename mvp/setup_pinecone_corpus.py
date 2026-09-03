"""
One-time setup: embed the tariff corpus and upload it to Pinecone.

Run this ONCE before using the Geopolitical Risk module in the app.
Re-run only if you edit tariff_corpus.py.

Requires:
    OPENAI_API_KEY   -- for generating embeddings (text-embedding-3-small)
    PINECONE_API_KEY -- for creating/writing to the index

Usage:
    python setup_pinecone_corpus.py
"""

import os
import time
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from tariff_corpus import TARIFF_CORPUS

INDEX_NAME = "geopolitical-risk-corpus"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536


def main():
    openai_key = os.environ.get("OPENAI_API_KEY")
    pinecone_key = os.environ.get("PINECONE_API_KEY")
    if not openai_key or not pinecone_key:
        raise EnvironmentError(
            "Both OPENAI_API_KEY and PINECONE_API_KEY must be set as environment variables."
        )

    openai_client = OpenAI(api_key=openai_key)
    pc = Pinecone(api_key=pinecone_key)

    existing_indexes = [idx.name for idx in pc.list_indexes()]
    if INDEX_NAME not in existing_indexes:
        print(f"Creating index '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        # Serverless index creation is async -- wait until it's ready
        while not pc.describe_index(INDEX_NAME).status["ready"]:
            time.sleep(1)
        print("Index created.")
    else:
        print(f"Index '{INDEX_NAME}' already exists -- reusing it.")

    index = pc.Index(INDEX_NAME)

    print(f"Embedding {len(TARIFF_CORPUS)} snippets...")
    vectors = []
    for snippet in TARIFF_CORPUS:
        embedding_response = openai_client.embeddings.create(
            model=EMBEDDING_MODEL, input=snippet["text"]
        )
        vector = embedding_response.data[0].embedding
        vectors.append({
            "id": snippet["id"],
            "values": vector,
            "metadata": {
                "text": snippet["text"],
                "country": snippet["country"],
                "category": snippet["category"],
                "source": snippet["source"],
            },
        })

    print("Upserting to Pinecone...")
    index.upsert(vectors=vectors)

    stats = index.describe_index_stats()
    print(f"\nDone. Index now contains {stats['total_vector_count']} vectors.")


if __name__ == "__main__":
    main()
