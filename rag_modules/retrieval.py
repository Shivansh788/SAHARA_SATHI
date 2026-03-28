import numpy as np


def _doc_text(doc):
    if isinstance(doc, dict):
        return doc.get("text", "")
    return str(doc)


def embed(text, model):
    return model.encode(text)


def dense_search(query, index, docs, model, k=10):
    q_vec = np.array([embed(query, model)]).astype("float32")
    _, idx = index.search(q_vec, k)
    return [docs[i] for i in idx[0] if 0 <= i < len(docs)]


def bm25_search(query, bm25, docs, k=10):
    scores = bm25.get_scores(query.split())
    top_k = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    return [docs[i] for i in top_k]


def prepare_embedding_texts(docs):
    return [_doc_text(doc) for doc in docs]