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

EMBEDDINGS:OllamaEmbeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_langchain_db"

def db_intitalise(content_key:str, jq_schema:str, src_file_path:str, extract_meta_func:Callable , embed_func:OllamaEmbeddings, collection_name:str, db_location:str="./chroma_langchain_db") -> Chroma:
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
            metadata_func=extract_meta_func,
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
    
meta_store = db_intitalise(content_key="definition", jq_schema=".metakeys[]", src_file_path="./resources/metakeys.json", extract_meta_func=extract_metakeys, embed_func=EMBEDDINGS, collection_name="netwitness_meta_keys")
meta_retriever = meta_store.as_retriever(search_kwargs={"k": 5})
