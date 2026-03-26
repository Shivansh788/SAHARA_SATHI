def rrf_fusion(bm25_results, dense_results):
    combined = {}

    for rank, doc in enumerate(bm25_results):
        combined[doc] = combined.get(doc, 0) + 1/(rank+1)

    for rank, doc in enumerate(dense_results):
        combined[doc] = combined.get(doc, 0) + 1/(rank+1)

    sorted_docs = sorted(combined.items(), key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in sorted_docs[:5]]