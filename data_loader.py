import pandas as pd
from rank_bm25 import BM25Okapi
import pickle
import os

def load_data():
    if os.path.exists("rag_data.pkl"):
        try:
            with open("rag_data.pkl", "rb") as f:
                documents, bm25 = pickle.load(f)
            return documents, bm25
        except Exception as e:
            print(f"Error loading cached RAG data: {e}. Recomputing...")

    gov = pd.read_csv("data/Gov_schemes.csv")
    ngo = pd.read_csv("data/ngo_data.csv")

    data = pd.concat([gov, ngo], ignore_index=True)

    documents = []
    for _, row in data.iterrows():
        text = " ".join([str(v) for v in row.values])
        documents.append(text)

    tokenized_corpus = [doc.split(" ") for doc in documents]
    bm25 = BM25Okapi(tokenized_corpus)

    with open("rag_data.pkl", "wb") as f:
        pickle.dump((documents, bm25), f)

    return documents, bm25