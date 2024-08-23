import json
from pathlib import Path
from typing import NamedTuple
from urllib.parse import urlparse

from loaders import load_dir, load_file, load_sparql
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import RDF, XSD
from renderers import render_visjs

BNODE_KLASS = URIRef("bnode")


class Node(NamedTuple):
    id: int
    label: str
    isliteral: bool = False
    isblank: bool = False


class Edge(NamedTuple):
    from_id: int
    to_id: int
    label: str


class Diagram:
    def __init__(self, focus_node: URIRef = None):
        self.nodes: set[Node] = set()
        self.edges: set[Edge] = set()
        self.serialization: dict = {}
        self.overrides: dict = {}
        self._store: Graph = Graph()

    def parse(
        self,
        source: str,
        iri: str | None,
        graph: str | None,
        username: str | None,
        password: str | None,
    ):
        if urlparse(source).netloc:
            self._store = load_sparql(
                endpoint=source,
                iri=iri,
                graph=graph,
                username=username,
                password=password,
            )
        elif Path(source).is_dir():
            self._store = load_dir(source)
        elif Path(source).is_file():
            self._store = load_file(source)
        else:
            raise NotImplementedError
        if iri:
            self._parse_instance()
        else:
            self._parse_classes()

    def _parse_classes(self):
        klasses = self._store.objects(None, RDF.type, unique=True)
        for klass in klasses:
            klass_id = hash(klass)
            klass_label = klass.n3(self._store.namespace_manager)
            self.nodes.add(Node(id=klass_id, label=klass_label))
            instances = self._store.subjects(RDF.type, klass, unique=True)
            for instance in instances:
                # get outgoing connections
                pred_obs = self._store.predicate_objects(instance, unique=True)
                for pred, obj in pred_obs:
                    if pred == RDF.type:
                        continue
                    isliteral = False
                    isblank = False
                    obj_klass = self._store.value(obj, RDF.type, None)
                    if isinstance(obj, Literal):
                        isliteral = True
                        obj_klass = obj.datatype if obj.datatype else XSD.string
                    elif isinstance(obj, BNode):
                        if not obj_klass:
                            obj_klass = BNODE_KLASS
                            isblank = True
                    obj_id = hash(obj_klass)
                    if isblank or isliteral:
                        obj_label = obj_klass.n3(self._store.namespace_manager)
                        self.nodes.add(
                            Node(
                                id=obj_id,
                                label=obj_label,
                                isliteral=isliteral,
                                isblank=isblank,
                            )
                        )
                    pred_label = pred.n3(self._store.namespace_manager)
                    self.edges.add(
                        Edge(from_id=klass_id, to_id=obj_id, label=pred_label)
                    )
                # get incoming connections
                subj_preds = self._store.subject_predicates(instance, unique=True)
                for subj, pred in subj_preds:
                    isblank = False
                    subj_klass = self._store.value(subj, RDF.type, None)
                    if isinstance(subj, BNode):
                        if not subj_klass:
                            subj_klass = BNODE_KLASS
                            isblank = True
                    subj_id = hash(subj_klass)
                    if isblank:
                        subj_label = subj_klass.n3(self._store.namespace_manager)
                        self.nodes.add(
                            Node(id=subj_id, label=subj_label, isblank=isblank)
                        )
                    pred_label = pred.n3(self._store.namespace_manager)
                    self.edges.add(
                        Edge(from_id=subj_id, to_id=klass_id, label=pred_label)
                    )

    def _parse_instance(self):
        # TODO: implement instance level query
        raise NotImplementedError

    def serialize(self) -> str:
        self.serialization["nodes"] = [
            {
                "id": node.id,
                "label": node.label,
                "isliteral": node.isliteral,
                "isblank": node.isblank,
            }
            for node in self.nodes
        ]
        self.serialization["edges"] = [
            {"from": edge.from_id, "to": edge.to_id, "label": edge.label}
            for edge in self.edges
        ]
        return json.dumps(self.serialization)

    def render(self, format: str):
        if not self.serialization:
            self.serialize()
        if format == "visjs":
            render_visjs(self.serialization, self.overrides)
        else:
            raise NotImplementedError
