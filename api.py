from fastapi import FastAPI
from data_loader import load_data
from rag_modules.intake import intake_agent
from rag_modules.retrieval import dense_search, bm25_search, embed
from rag_modules.fusion import rrf_fusion
from rag_modules.reranker import rerank
from rag_modules.synthesis import generate
import faiss
import numpy as np

app = FastAPI()

from coeai import LLMinfer

# transformers pipeline removed to avoid 2.2GB download
pipeline = None


# Initialize client (requires UPESNET connectivity)
# PLACEHOLDER: Enter your COEAI API key here
llm = LLMinfer(api_key="coeai-_9d5O7c-ei761wsqowkhmBNxPeaP-wIP")

chat_history = {}

# Local generative model removed to avoid large downloads
local_pipeline = None


docs, bm25 = load_data()

# build FAISS
embeddings = [embed(d) for d in docs]
dim = len(embeddings[0])
index = faiss.IndexFlatL2(dim)
index.add(np.array(embeddings).astype("float32"))


@app.post("/ask")
def ask(query: str, session_id: str = "default"):

    profile = intake_agent(query)
    
    history = chat_history.get(session_id, [])

    bm25_res = bm25_search(query, bm25, docs)
    dense_res = dense_search(query, index, docs)

    fused = rrf_fusion(bm25_res, dense_res)
    final_docs = rerank(query, fused)

    answer = generate(query, "\n".join(final_docs), profile, llm, local_pipeline=local_pipeline, history=history)

    history.append({"user": query, "assistant": answer})
    chat_history[session_id] = history

    return {
        "answer": answer,
        "mode": "citizen"
    }