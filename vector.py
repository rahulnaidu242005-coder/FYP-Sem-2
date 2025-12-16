from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd
 
embeddings = OllamaEmbeddings(model="nomic-embed-text")
 
db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)
df = pd.read_csv("resources/API.csv")
 
if add_documents:
    documents = []
    ids = []
 
    for i, row in df.iterrows():
        document = Document(
            page_content=(
                "Question: " + row["question"] + "\n"
                "API: " + row["answer"]
            ),
            metadata={
                "id": str(i)
            },
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)

vector_store = Chroma(
    collection_name="netwitness_api_docs",
    persist_directory=db_location,
    embedding_function=embeddings,
)
 
if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)
 
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)