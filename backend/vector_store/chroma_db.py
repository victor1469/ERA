import os
import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


CHROMA_PATH = os.path.join(
    BASE_DIR,
    "chroma_data"
)


# Embedding模型
model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5"
)


# Chroma数据库
client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = client.get_or_create_collection(
    name="document_chunks"
)



def add_documents(chunks,filename):

    embeddings = model.encode(
        chunks,
        normalize_embeddings=True
    )


    ids = [
        f"{filename}_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=[
            {
                "filename": filename
            }
            for _ in chunks
        ]
    )


    return len(chunks)



def search_documents(
    query,
    top_k=5
):

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )


    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )


    return results


def delete_documents(filename):

    results = collection.get(
        where={
            "filename": filename
        }
    )


    ids = results["ids"]


    if len(ids) > 0:

        collection.delete(
            ids=ids
        )


    return len(ids)