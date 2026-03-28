import re
from collections import defaultdict
from typing import Dict, List, Tuple


def _slugify(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "unknown"


def _split_multi(value: str) -> List[str]:
    if not value:
        return []
    parts = re.split(r"[,|/]", str(value))
    cleaned = []
    for p in parts:
        item = p.strip()
        if item:
            cleaned.append(item)
    return cleaned


def _add_node(nodes: Dict[str, Dict], node_id: str, label: str, node_type: str, metadata: Dict = None) -> None:
    if node_id in nodes:
        return
    nodes[node_id] = {
        "id": node_id,
        "label": label,
        "type": node_type,
        "metadata": metadata or {},
    }


def _add_edge(edges: List[Dict], seen_edges: set, source: str, target: str, relation: str) -> None:
    key = (source, target, relation)
    if key in seen_edges:
        return
    seen_edges.add(key)
    edges.append({
        "source": source,
        "target": target,
        "relation": relation,
    })


def build_graph_data(
    schemes: List[Dict],
    ngos: List[Dict],
    max_schemes: int = 450,
    max_ngos: int = 250,
    max_cross_links_per_scheme: int = 5,
) -> Dict:
    nodes: Dict[str, Dict] = {}
    edges: List[Dict] = []
    seen_edges = set()

    schemes_slice = schemes[:max_schemes]
    ngos_slice = ngos[:max_ngos]

    category_to_scheme_ids: Dict[str, List[str]] = defaultdict(list)
    category_to_ngo_ids: Dict[str, List[str]] = defaultdict(list)

    # Build scheme nodes and connect scheme -> category
    for idx, scheme in enumerate(schemes_slice):
        scheme_name = scheme.get("scheme_name", "Unnamed Scheme")
        scheme_id = f"scheme:{_slugify(scheme.get('slug') or f'{scheme_name}-{idx}') }"
        _add_node(
            nodes,
            scheme_id,
            scheme_name,
            "scheme",
            {
                "level": scheme.get("level", ""),
                "category": scheme.get("category", ""),
                "description": scheme.get("description", ""),
            },
        )

        categories = _split_multi(scheme.get("category", "")) or ["General"]
        for category in categories:
            cat_id = f"category:{_slugify(category)}"
            _add_node(nodes, cat_id, category, "category")
            _add_edge(edges, seen_edges, scheme_id, cat_id, "belongs_to_category")
            category_to_scheme_ids[cat_id].append(scheme_id)

    # Build NGO nodes and connect ngo -> category + ngo -> location
    for idx, ngo in enumerate(ngos_slice):
        ngo_name = ngo.get("name", "Unnamed NGO")
        ngo_id = f"ngo:{_slugify(f'{ngo_name}-{idx}') }"
        _add_node(
            nodes,
            ngo_id,
            ngo_name,
            "ngo",
            {
                "location": ngo.get("location", ""),
                "category": ngo.get("category", ""),
                "description": ngo.get("description", ""),
            },
        )

        ngo_category = ngo.get("category", "General") or "General"
        cat_id = f"category:{_slugify(ngo_category)}"
        _add_node(nodes, cat_id, ngo_category, "category")
        _add_edge(edges, seen_edges, ngo_id, cat_id, "supports_category")
        category_to_ngo_ids[cat_id].append(ngo_id)

        location = ngo.get("location", "Unknown") or "Unknown"
        loc_id = f"location:{_slugify(location)}"
        _add_node(nodes, loc_id, location, "location")
        _add_edge(edges, seen_edges, ngo_id, loc_id, "operates_in")

    # Cross-link schemes with NGOs through shared categories.
    for cat_id, scheme_ids in category_to_scheme_ids.items():
        ngo_ids = category_to_ngo_ids.get(cat_id, [])
        if not ngo_ids:
            continue
        for scheme_id in scheme_ids:
            for ngo_id in ngo_ids[:max_cross_links_per_scheme]:
                _add_edge(edges, seen_edges, scheme_id, ngo_id, "can_get_help_from")

    graph = {
        "nodes": list(nodes.values()),
        "edges": edges,
        "stats": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "scheme_count": len(schemes_slice),
            "ngo_count": len(ngos_slice),
        },
    }
    return graph


def filter_graph(graph: Dict, query: str, node_limit: int = 120, edge_limit: int = 220) -> Dict:
    query_l = (query or "").strip().lower()
    if not query_l:
        return {
            "nodes": graph.get("nodes", [])[:node_limit],
            "edges": graph.get("edges", [])[:edge_limit],
            "stats": graph.get("stats", {}),
            "query": "",
        }

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    matched_node_ids = set()
    for node in nodes:
        label = str(node.get("label", "")).lower()
        node_type = str(node.get("type", "")).lower()
        metadata = " ".join([str(v).lower() for v in node.get("metadata", {}).values()])
        if query_l in label or query_l in node_type or query_l in metadata:
            matched_node_ids.add(node["id"])

    # Expand one hop around matched nodes to keep structure meaningful.
    expanded_ids = set(matched_node_ids)
    for edge in edges:
        if edge["source"] in matched_node_ids or edge["target"] in matched_node_ids:
            expanded_ids.add(edge["source"])
            expanded_ids.add(edge["target"])

    filtered_nodes = [n for n in nodes if n["id"] in expanded_ids][:node_limit]
    filtered_ids = {n["id"] for n in filtered_nodes}
    filtered_edges = [
        e for e in edges
        if e["source"] in filtered_ids and e["target"] in filtered_ids
    ][:edge_limit]

    return {
        "nodes": filtered_nodes,
        "edges": filtered_edges,
        "stats": graph.get("stats", {}),
        "query": query,
    }
