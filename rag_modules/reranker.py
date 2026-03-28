def _doc_text(doc):
    if isinstance(doc, dict):
        return doc.get("text", "")
    return str(doc)


def _score_with_cross_encoder(query, docs, cross_encoder_model):
    pairs = [[query, _doc_text(doc)] for doc in docs]
    scores = cross_encoder_model.predict(pairs)
    ranked = sorted(zip(docs, scores), key=lambda x: float(x[1]), reverse=True)
    output = []
    for doc, score in ranked:
        if isinstance(doc, dict):
            enriched = dict(doc)
            enriched["rerank_score"] = float(score)
            output.append(enriched)
        else:
            output.append({"text": str(doc), "rerank_score": float(score)})
    return output


def rerank(query, docs, cross_encoder_model=None, top_k=5):
    if not docs:
        return []

    if cross_encoder_model is not None:
        try:
            ranked_docs = _score_with_cross_encoder(query, docs, cross_encoder_model)
            return ranked_docs[:top_k]
        except Exception as exc:
            print(f"Cross-encoder reranking failed, falling back to heuristic: {exc}")

    # Safe fallback: lexical hit ranking when cross-encoder is unavailable.
    sorted_docs = sorted(
        docs,
        key=lambda x: query.lower() in _doc_text(x).lower(),
        reverse=True,
    )
    fallback = []
    for doc in sorted_docs[:top_k]:
        if isinstance(doc, dict):
            enriched = dict(doc)
            enriched.setdefault("rerank_score", 0.0)
            fallback.append(enriched)
        else:
            fallback.append({"text": str(doc), "rerank_score": 0.0})
    return fallback