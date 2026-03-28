from typing import Any, Dict, List

import requests

import config


def _flatten_dict(record: Dict[str, Any], max_fields: int = 12) -> str:
    pairs = []
    count = 0
    for key, value in record.items():
        if value is None or str(value).strip() == "":
            continue
        pairs.append(f"{key}: {value}")
        count += 1
        if count >= max_fields:
            break
    return " | ".join(pairs)


def _normalize_resources(resources: List[Dict[str, Any]], source_name: str) -> List[Dict[str, Any]]:
    docs: List[Dict[str, Any]] = []
    for i, item in enumerate(resources, start=1):
        title = item.get("title") or item.get("name") or item.get("resource_name") or f"DataGov Resource {i}"
        description = item.get("description") or item.get("desc") or ""
        category = item.get("sector") or item.get("category") or item.get("theme") or ""
        item_id = item.get("id") or item.get("resource_id") or f"resource-{i}"
        combined_text = _flatten_dict(item)

        docs.append(
            {
                "id": f"datagov::{item_id}",
                "source_type": "data_gov",
                "source_name": f"{source_name} | {title}",
                "category": str(category),
                "text": (
                    f"Type: DataGov | Title: {title} | Description: {description} | "
                    f"Details: {combined_text}"
                ),
            }
        )
    return docs


def _extract_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    for key in ("resources", "records", "results", "data", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return [v for v in value if isinstance(v, dict)]
    return []


def _official_search(query: str, limit: int):
    api_key = (config.DATA_GOV_API_KEY or "").strip()
    if not api_key:
        return [], {"provider": "official", "status": "skipped", "message": "DATA_GOV_API_KEY not configured"}

    base = config.DATA_GOV_BASE_URL.rstrip("/")
    url = f"{base}/catalog/v1/resources"
    params = {
        "api-key": api_key,
        "format": "json",
        "limit": int(limit),
        "offset": 0,
        "q": query,
        "query": query,
    }

    try:
        response = requests.get(url, params=params, timeout=config.DATA_GOV_TIMEOUT_SEC)
        if response.status_code != 200:
            return [], {"provider": "official", "status": response.status_code, "message": response.text[:220]}
        payload = response.json() if response.content else {}
        items = _extract_items(payload if isinstance(payload, dict) else {})
        docs = _normalize_resources(items[:limit], "data.gov.in")
        return docs, {"provider": "official", "status": 200, "count": len(docs)}
    except Exception as exc:
        return [], {"provider": "official", "status": "error", "message": str(exc)}


def _rapidapi_search(query: str, limit: int):
    key = (config.DATA_GOV_RAPIDAPI_KEY or "").strip()
    if not key:
        return [], {"provider": "rapidapi", "status": "skipped", "message": "DATA_GOV_RAPIDAPI_KEY not configured"}

    base = config.DATA_GOV_RAPIDAPI_BASE_URL.rstrip("/")
    host = config.DATA_GOV_RAPIDAPI_HOST

    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": host,
    }

    candidate_paths = ["/search", "/datasets/search", "/v1/search", "/catalog/search"]
    params = {"q": query, "query": query, "limit": int(limit)}

    attempts: List[Dict[str, Any]] = []
    for path in candidate_paths:
        url = f"{base}{path}"
        try:
            response = requests.get(url, headers=headers, params=params, timeout=config.DATA_GOV_TIMEOUT_SEC)
            if response.status_code != 200:
                attempts.append({"path": path, "status": response.status_code, "message": response.text[:180]})
                continue
            payload = response.json() if response.content else {}
            items = _extract_items(payload if isinstance(payload, dict) else {})
            docs = _normalize_resources(items[:limit], "data.gov.in (RapidAPI)")
            if docs:
                return docs, {"provider": "rapidapi", "status": 200, "path": path, "count": len(docs)}
            attempts.append({"path": path, "status": 200, "count": 0})
        except Exception as exc:
            attempts.append({"path": path, "status": "error", "message": str(exc)})
            continue

    return [], {"provider": "rapidapi", "attempts": attempts}


def is_configured() -> bool:
    provider = config.DATA_GOV_PROVIDER
    if provider == "official":
        return bool((config.DATA_GOV_API_KEY or "").strip())
    if provider == "rapidapi":
        return bool((config.DATA_GOV_RAPIDAPI_KEY or "").strip())
    return bool((config.DATA_GOV_API_KEY or "").strip() or (config.DATA_GOV_RAPIDAPI_KEY or "").strip())


def search_data_gov(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    if not query or not query.strip():
        return []

    provider = config.DATA_GOV_PROVIDER
    if provider == "official":
        return _official_search(query, limit)[0]
    if provider == "rapidapi":
        return _rapidapi_search(query, limit)[0]

    # auto mode: try official first, then rapidapi
    docs, _ = _official_search(query, limit)
    if docs:
        return docs
    return _rapidapi_search(query, limit)[0]


def debug_data_gov_search(query: str, limit: int = 5) -> Dict[str, Any]:
    provider = config.DATA_GOV_PROVIDER
    if not query or not query.strip():
        return {"provider": provider, "results": [], "diagnostics": [{"message": "query is empty"}]}

    if provider == "official":
        docs, meta = _official_search(query, limit)
        return {"provider": provider, "results": docs, "diagnostics": [meta]}

    if provider == "rapidapi":
        docs, meta = _rapidapi_search(query, limit)
        return {"provider": provider, "results": docs, "diagnostics": [meta]}

    official_docs, official_meta = _official_search(query, limit)
    if official_docs:
        return {"provider": "auto", "results": official_docs, "diagnostics": [official_meta]}

    rapid_docs, rapid_meta = _rapidapi_search(query, limit)
    return {
        "provider": "auto",
        "results": rapid_docs,
        "diagnostics": [official_meta, rapid_meta],
    }
