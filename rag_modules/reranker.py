def rerank(query, docs):
    # simple heuristic reranking (replace later with cross-encoder)
    return sorted(docs, key=lambda x: query.lower() in x.lower(), reverse=True)