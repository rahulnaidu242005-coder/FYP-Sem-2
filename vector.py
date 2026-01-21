from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import JSONLoader
import os
from pathlib import Path
from typing import Callable
from lib.API_Modules import NetWitnessClient, LoggerCustom

def extract_metakeys(record: dict, metadata: dict) -> dict:
    metadata["metakey"] = record["key"]
    return metadata

EMBEDDINGS = OllamaEmbeddings(model="mxbai-embed-large", base_url="http://bazzite.tail3be278.ts.net:11434")

db_location = "./chroma_langchain_db"

def db_intitalise(content_key:str, jq_schema:str, src_file_path:str, embed_func:Callable, collection_name:str, db_location:str="./chroma_langchain_db") -> Chroma:
    """Initialises or loads a Chroma vector DB from JSON documents.
    Args:
        content_key (str): Key in JSON to use as document content.
        jq_schema (str): JQ schema to extract records from JSON.
        src_file_path (str): Path to the source JSON file.
        embed_func (function): Embedding function to use.
        collection_name (str): Name of the Chroma collection.
        db_location (str, optional): Directory to persist the DB. Defaults to "./chroma_langchain_db".
    Returns:
        Chroma vector store instance.
    """
    # Check if persisted DB exists and has data
    if os.path.exists(db_location) and os.listdir(db_location):  # Better check than count()
        meta_store = Chroma(
            collection_name=collection_name,
            persist_directory=db_location,
            embedding_function=embed_func
        )
        print(f"Database loaded from disk. Contains {meta_store._collection.count()} documents.")
    else:
        print("Building new DB...")
        loader = JSONLoader(
            file_path=src_file_path,
            jq_schema=jq_schema,
            metadata_func=embed_func,
            content_key=content_key
        )
        loaded_data = loader.load()
        meta_store = Chroma.from_documents(
            documents=loaded_data,
            embedding=embed_func,
            persist_directory=db_location,
            collection_name=collection_name
        )
        print(f"Successfully indexed {len(loaded_data)} documents.")
    return meta_store
    
meta_store = db_intitalise(content_key="definition", jq_schema=".metakeys[]", src_file_path="./resources/metakeys.json", embed_func=EMBEDDINGS, collection_name="netwitness_meta_keys")
meta_retriever = meta_store.as_retriever(search_kwargs={"k": 5})

# BASE_DIR = Path(__file__).resolve().parent
# df = pd.read_csv(BASE_DIR / "resources" / "API.csv")
#
# # ADDED: load metakeys.csv (columns: key, definition)
# df_meta = pd.read_csv(BASE_DIR / "resources" / "metakeys.csv")
# #
# #
# def extract_metakeys(record: dict, metadata: dict) -> dict:
#     metadata["metakey"] = record["key"]
#     return metadata



# retriever = vector_store.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 15},
# )
# #
# # # ADDED: separate DB for metakeys
# # db_location_meta = "./chroma_langchain_db_meta"
# # add_documents_meta = not os.path.exists(db_location_meta)
# #
# #
# # if add_documents:
# #     documents = []
# #     ids = []
# #
# #     for i, row in df.iterrows():
# #         document = Document(
# #             page_content=(
# #                 "Question: " + str(row["question"]).strip() + "\n"
# #                 "Answer: " + str(row["answer"]).strip()
# #             ),
# #             metadata={
# #                 "id": str(i)
# #             },
# #             id=str(i)
# #         )
# #         ids.append(str(i))
# #         documents.append(document)
# #
# # # ADDED: build metakeys documents using key/definition
# # if add_documents_meta:
# #     meta_documents = []
# #     meta_ids = []
# #
# #     for i, row in df_meta.iterrows():
# #         meta_document = Document(
# #             page_content=(
# #                 "Key: " + str(row["key"]).strip() + "\n"
# #                 "Definition: " + str(row["definition"]).strip()
# #             ),
# #             metadata={
# #                 "id": str(i)
# #             },
# #             id=str(i)
# #         )
# #         meta_ids.append(str(i))
# #         meta_documents.append(meta_document)
# #
# #
# # vector_store = Chroma(
# #     collection_name="netwitness_api_docs",
# #     persist_directory=db_location,
# #     embedding_function=embeddings,
# # )
# #
# # # ADDED: separate collection for metakeys
# # meta_vector_store = Chroma(
# #     collection_name="netwitness_meta_keys",
# #     persist_directory=db_location_meta,
# #     embedding_function=embeddings,
# # )
# #
# #
# # if add_documents:
# #     vector_store.add_documents(documents=documents, ids=ids)
# #
# # # ADDED: persist metakeys docs
# # if add_documents_meta:
# #     meta_vector_store.add_documents(documents=meta_documents, ids=meta_ids)
# #
# #
# # retriever = vector_store.as_retriever(
# #     search_kwargs={"k": 1}
# # )
# #
# # # ADDED: metakeys retriever
# # meta_retriever = meta_vector_store.as_retriever(
# #     search_kwargs={"k": 3}
# # )
