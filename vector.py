from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "resources" / "API.csv")

# ADDED: load metakeys.csv (columns: key, definition)
df_meta = pd.read_csv(BASE_DIR / "resources" / "metakeys.csv")


embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)

# ADDED: separate DB for metakeys
db_location_meta = "./chroma_langchain_db_meta"
add_documents_meta = not os.path.exists(db_location_meta)


if add_documents:
    documents = []
    ids = []

    for i, row in df.iterrows():
        document = Document(
            page_content=(
                "Question: " + str(row["question"]).strip() + "\n"
                "Answer: " + str(row["answer"]).strip()
            ),
            metadata={
                "id": str(i)
            },
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)

# ADDED: build metakeys documents using key/definition
if add_documents_meta:
    meta_documents = []
    meta_ids = []

    for i, row in df_meta.iterrows():
        meta_document = Document(
            page_content=(
                "Key: " + str(row["key"]).strip() + "\n"
                "Definition: " + str(row["definition"]).strip()
            ),
            metadata={
                "id": str(i)
            },
            id=str(i)
        )
        meta_ids.append(str(i))
        meta_documents.append(meta_document)


vector_store = Chroma(
    collection_name="netwitness_api_docs",
    persist_directory=db_location,
    embedding_function=embeddings,
)

# ADDED: separate collection for metakeys
meta_vector_store = Chroma(
    collection_name="netwitness_meta_keys",
    persist_directory=db_location_meta,
    embedding_function=embeddings,
)


if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

# ADDED: persist metakeys docs
if add_documents_meta:
    meta_vector_store.add_documents(documents=meta_documents, ids=meta_ids)


retriever = vector_store.as_retriever(
    search_kwargs={"k": 1}
)

# ADDED: metakeys retriever
meta_retriever = meta_vector_store.as_retriever(
    search_kwargs={"k": 3}
)
