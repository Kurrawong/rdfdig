import json
from pathlib import Path

from jinja2 import Template
from rdflib import Graph

added_node_ids = set()
nodes = []
edges = []
options = dict()


template = Template(Path("template.html").read_text())
source = Path("sites_2024-08-15.ttl")

g = Graph().parse(source=source)

query = """
select distinct ?klass ?predicate ?other_klass
where {
    ?s a ?klass .
    ?s ?predicate ?o .
    ?o a ?other_klass .
}
"""
result = g.query(query)
for result in result.bindings:
    klass = result["klass"]
    klass_id = hash(klass)
    klass_label = klass.n3(g.namespace_manager)

    other_klass = result["other_klass"]
    other_klass_id = hash(other_klass)
    other_klass_label = other_klass.n3(g.namespace_manager)

    predicate = result["predicate"]
    predicate_label = predicate.n3(g.namespace_manager)

    if klass_id not in added_node_ids:
        nodes.append({"id": klass_id, "label": klass_label})
        added_node_ids.add(klass_id)
    if other_klass_id not in added_node_ids:
        nodes.append({"id": other_klass_id, "label": other_klass_label})
        added_node_ids.add(other_klass_id)

    edges.append({"from": other_klass_id, "to": klass_id, "label": predicate_label})

nodes = json.dumps(nodes)
edges = json.dumps(edges)

Path("rendered.html").write_text(
    template.render(nodes=nodes, edges=edges, options=options)
)
