import json


def serialize_visjs(nodes: list, edges: list) -> str:
    serialization = dict()
    serialization["nodes"] = [{"id": node, "label": label} for node, label in nodes]
    serialization["edges"] = [
        {"from": from_node, "to": to_node, "label": predicate}
        for from_node, to_node, predicate in edges
    ]
    return json.dumps(serialization)
