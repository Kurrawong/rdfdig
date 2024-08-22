from pathlib import Path
from urllib.parse import urlparse

from loaders import load_dir, load_file, load_sparql
from rdflib import Graph, URIRef
from renderers import render_visjs
from serializers import serialize_visjs


class Diagram:
    def __init__(self, focus_node: URIRef = None):
        self.nodes: list[tuple[int, str]] = []
        self.edges: list[tuple[int, int, str]] = []
        self.options: dict = {}
        self._graph: Graph = Graph()
        self._serialization: str = None
        self._format: str = None

    def parse(
        self,
        source: str,
        iri: str | None,
        graph: str | None,
        username: str | None,
        password: str | None,
    ):
        if urlparse(source).netloc:
            self._graph = load_sparql(
                endpoint=source,
                iri=iri,
                graph=graph,
                username=username,
                password=password,
            )
        elif Path(source).is_dir():
            self._graph = load_dir(source)
        elif Path(source).is_file():
            self._graph = load_file(source)
        else:
            raise NotImplementedError
        if iri:
            self._parse_instance()
        else:
            self._parse_classes()

    def _parse_classes(self):
        query = (Path(__file__).parent / "queries" / "classes.rq").read_text()
        results = self._graph.query(query)
        for result in results.bindings:
            klass = result["class"]
            klass_id = hash(klass)
            klass_label = klass.n3(self._graph.namespace_manager)
            node = (klass_id, klass_label)

            other_klass = result["other_class"]
            other_klass_id = hash(other_klass)
            other_klass_label = other_klass.n3(self._graph.namespace_manager)
            other_node = (other_klass_id, other_klass_label)

            predicate = result["predicate"]
            predicate_label = predicate.n3(self._graph.namespace_manager)
            edge = (klass_id, other_klass_id, predicate_label)

            if node not in self.nodes:
                self.nodes.append(node)
            if other_node not in self.nodes:
                self.nodes.append(other_node)
            if edge not in self.edges:
                self.edges.append(edge)

    def _parse_instance(self):
        raise NotImplementedError

    def serialize(self, format: str):
        if self._format != format:
            if format == "visjs":
                self._serialization = serialize_visjs(
                    nodes=self.nodes, edges=self.edges
                )
            else:
                raise NotImplementedError
        self._format = format
        return self._serialization

    def render(self, format: str):
        if not self._serialization or self._format != format:
            self.serialize(format=format)
        if format == "visjs":
            render_visjs(self._serialization, options=self.options)
        else:
            raise NotImplementedError
