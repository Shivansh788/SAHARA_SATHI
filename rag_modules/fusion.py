def _doc_key(doc):
    """Build a stable, hashable key for a document."""
    if isinstance(doc, dict):
        # Prefer explicit IDs when present.
        if doc.get("id"):
            return f"id::{doc.get('id')}"
        source = doc.get("source_name", "")
        category = doc.get("category", "")
        text = doc.get("text", "")
        # Fallback key from deterministic content slices.
        return f"doc::{source}::{category}::{text[:200]}"
    return f"raw::{str(doc)[:220]}"


def rrf_fusion(bm25_results, dense_results, top_k=50, rrf_k=60):
    combined_scores = {}
    key_to_doc = {}

    for rank, doc in enumerate(bm25_results):
        key = _doc_key(doc)
        key_to_doc[key] = doc
        combined_scores[key] = combined_scores.get(key, 0.0) + 1 / (rrf_k + rank + 1)

    for rank, doc in enumerate(dense_results):
        key = _doc_key(doc)
        key_to_doc[key] = doc
        combined_scores[key] = combined_scores.get(key, 0.0) + 1 / (rrf_k + rank + 1)

    sorted_keys = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    return [key_to_doc[key] for key, _ in sorted_keys[:top_k]]