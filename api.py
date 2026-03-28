from fastapi import FastAPI
import os
from data_loader import load_data
from rag_modules.intake import intake_agent
from rag_modules.retrieval import dense_search, bm25_search, prepare_embedding_texts
from rag_modules.fusion import rrf_fusion
from rag_modules.reranker import rerank
from rag_modules.synthesis import generate
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI()

try:
    from coeai import LLMinfer  # Optional paid fallback.
except Exception:
    LLMinfer = None

# transformers pipeline removed to avoid 2.2GB download
pipeline = None


# Initialize client (requires UPESNET connectivity)
llm = None
if os.environ.get("COEAI_API_KEY") and LLMinfer is not None:
    try:
        llm = LLMinfer(api_key=os.environ.get("COEAI_API_KEY", ""))
    except Exception:
        llm = None

chat_history = {}

# Local generative model removed to avoid large downloads
local_pipeline = None


docs, bm25 = load_data()
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# build FAISS
embeddings = embed_model.encode(prepare_embedding_texts(docs))
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(np.array(embeddings).astype("float32"))


@app.post("/ask")
def ask(query: str, session_id: str = "default"):

    profile = intake_agent(query)
    
    history = chat_history.get(session_id, [])

    bm25_res = bm25_search(query, bm25, docs, k=50)
    dense_res = dense_search(query, index, docs, embed_model, k=50)

    fused = rrf_fusion(bm25_res, dense_res, top_k=50)
    final_docs = rerank(query, fused, top_k=5)

    answer_payload = generate(
        query,
        final_docs,
        profile,
        llm,
        local_pipeline=local_pipeline,
        history=history,
        mode="citizen",
    )

    history.append({"user": query, "assistant": answer_payload.get("answer", "")})
    chat_history[session_id] = history

    return answer_payload