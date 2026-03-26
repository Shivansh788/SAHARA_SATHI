import os
import faiss
import logging
import warnings
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from data_loader import load_data
from rag_modules import retrieval, reranker, synthesis
from sentence_transformers import SentenceTransformer
from coeai import LLMinfer

from frontend_html import html_content

# Suppress HuggingFace warnings so it boots silently
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

# transformers pipeline removed to avoid 2.2GB download
pipeline = None


app = FastAPI()

# Global state to hold our models in memory
RAG_DATA = {
    "chat_history": {}
}

@app.on_event("startup")
async def startup_event():
    print("Starting up Sahara RAG Pipeline...")
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    docs, bm25 = load_data()
    
    if os.path.exists('index.faiss'):
        index = faiss.read_index('index.faiss')
    else:
        doc_embeddings = embed_model.encode(docs)
        index = faiss.IndexFlatL2(doc_embeddings.shape[1])
        index.add(doc_embeddings)
        faiss.write_index(index, 'index.faiss')
        
    llm = LLMinfer(api_key="coeai-_9d5O7c-ei761wsqowkhmBNxPeaP-wIP")
    
    # Local generative model removed to avoid large downloads
    local_pipeline = None


    RAG_DATA["embed_model"] = embed_model
    RAG_DATA["docs"] = docs
    RAG_DATA["bm25"] = bm25
    RAG_DATA["index"] = index
    RAG_DATA["llm"] = llm
    RAG_DATA["local_pipeline"] = local_pipeline
    print("✅ Application is ready! Open http://localhost:8501 in your browser.")

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    # Serve the exact HTML you asked for
    return html_content

class AskRequest(BaseModel):
    query: str
    profile: str = "farmer"
    session_id: str = "default_session"

@app.post("/api/ask")
async def ask_assistant(req: AskRequest):
    try:
        # Get history
        history = RAG_DATA["chat_history"].get(req.session_id, [])

        # 1. Retrieval
        dense_results = retrieval.dense_search(req.query, RAG_DATA["index"], RAG_DATA["docs"], RAG_DATA["embed_model"])
        sparse_results = retrieval.bm25_search(req.query, RAG_DATA["bm25"], RAG_DATA["docs"])
        context = list(set(dense_results + sparse_results))
        
        # 2. Reranking
        ranked_context = reranker.rerank(req.query, context)
        
        # 3. Synthesis
        answer = synthesis.generate(
            req.query, ranked_context, req.profile, RAG_DATA["llm"],
            local_pipeline=RAG_DATA.get("local_pipeline"),
            history=history
        )
        
        # Update history
        history.append({"user": req.query, "assistant": answer})
        RAG_DATA["chat_history"][req.session_id] = history

        return {"answer": answer}
    except Exception as e:
        print(f"Error: {e}")
        return {"answer": "Error generating response. Please try again."}

if __name__ == "__main__":
    # We use 8501 so the port remains exactly the same as Streamlit for convenience
    uvicorn.run(app, host="0.0.0.0", port=8501)