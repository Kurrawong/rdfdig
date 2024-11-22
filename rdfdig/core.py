import json
from pathlib import Path
from typing import NamedTuple
from urllib.parse import urlparse

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import RDF, XSD

from rdfdig.loaders import load_dir, load_file, load_sparql
from rdfdig.renderers import render_mermaid, render_visjs
from rdfdig.utils import expand_uri

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
    """Instances of Diagram expose methods to parse, serialize and render RDF data to diagrams.

    Broadly, two methods of parsing the data for display have been implemented.

    Class diagram display (the default)

        This method of parsing is useful to get a high level overview of the
        rdf:type's of things in your data. It obscures the details of individual
        instances of classes to make it easier to see what classes have been
        defined and how they are connected to each other.

    Instance diagram display (used if the iri parameter is provided to the parse method)

        This is a more typical display of RDF data, focused around a given node,
        this method will show all direct incoming and outgoing statements about
        that resource. Blank nodes will be recursively evaluated such that indirect
        blank node statements are not orphaned.

    For more details about each method refer to their respective _parse_*() method.
    """

    def __init__(self):
        self.nodes: set[Node] = set()
        self.edges: set[Edge] = set()
        self.serialization: dict = {}
        self.overrides: dict = {}
        self._store: Graph = Graph()

    def parse(
        self,
        sources: list[str | Path],
        iri: str | None = None,
        graph: str | None = None,
        username: str | None = None,
        password: str | None = None,
        limit: int = 1000,
        offset: int = 0,
        cutoff: int = 10000,
        timeout: int = 5,
    ):
        """load data from the specified source and reduce it to nodes and edges.

        :param source: can be path like or url like if url it must be a SPARQL endpoint
        :param iri: generate an instance level diagram for the specified resource.
        :param graph: URI like. restrict the diagram to the specifed graph.
        :param username: username for HTTP basic authentication if required.
        :param password: password. if left blank then the user will be prompted.
        :param limit: SPARQL limit.
        :param offset: SPARQL offset.
        :param cutoff: cutoff for SPARQL queries. Only retrieve this many triples.
        :param timeout: HTTP timeout (in seconds) for SPARQL queries.
        """

        self._store = Graph()
        sparql_endpoints = 0
        for source in sources:
            if not isinstance(source, Path) and urlparse(source).netloc:
                if sparql_endpoints > 0:
                    raise ValueError(
                        "Loading from multiple SPARQL endpoints is not supported"
                    )
                graph = load_sparql(
                    endpoint=source,
                    iri=iri,
                    graph=graph,
                    username=username,
                    password=password,
                    limit=limit,
                    offset=offset,
                    cutoff=cutoff,
                    timeout=timeout,
                )
                sparql_endpoints += 1
            elif Path(source).is_dir():
                graph = load_dir(Path(source))
            elif Path(source).is_file():
                graph = load_file(Path(source))
            else:
                raise NotImplementedError

            self._store += graph
            [
                self._store.namespace_manager.bind(prefix=prefix, namespace=namespace)
                for prefix, namespace in graph.namespace_manager.namespaces()
            ]

        if iri:
            self._parse_instances(expand_uri(iri, self._store.namespace_manager))
        else:
            self._parse_classes()

    def _parse_classes(self):
        """parse class nodes and edges from the loaded RDF.

        only cares about classes (i.e., declarations of rdf:type).
        instances of the classes are not recorded.

        statements of the form

            <lawson> a schema:Person .
            <kurrawongAI> a schema:Organisation .
            <lawson> schema:name "Lawson" .
            <lawson> schema:knows <kurrawongAI> .

        would be reduced to

            schema:Person -- schema:knows --> schema:Organisation

        indicating that there are schema:Person rseources in the data that
        are connected to schema:Organisation resources via the
        schema:knows predicate.

        The above information is very useful when constructing SPARQL
        queries or just generally trying to inspect the form of an
        RDF model.
        """
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

    def _parse_instances(self, iri: URIRef):
        """parse instance nodes and edges from the loaded RDF.

        for a given resource idntifier (iri) parses the direct incoming
        and outgoing statements. recursively evaluating blank nodes so that
        statements about blank nodes are not orphaned.

        for example, with <uluru> as the given iri
        the following statements

            <uluru> a schema:Place ;
                schema:name "Uluru-Kata Tjuta National Park" ;
                geo:hasGeometry [
                    a geo:Geometry ;
                    geo:asWKT "POINT(-25.20426 131.02110)"^^geo:wktLiteral .
                ] .
            <lawson> a schema:Person ;
                schema:name "Lawson" .

        would be reduced to a diagram showing

            <uluru> -- a --> schema:Place
            <uluru> -- schema:Name --> Uluru-Kata Tjuta National Park
            <uluru> -- geo:hasGeometry --> _:1230409549305
            _:1230409549305 -- a -- > geo:Geometry
            _:1230409549305 -- geo:asWKT --> "POINT(-25.20426 131.02110)"^^geo:wktLiteral

        """
        iri_id = hash(iri)
        iri_label = iri.n3(self._store.namespace_manager)
        isblank = isinstance(iri, BNode)
        self.nodes.add(Node(id=iri_id, label=iri_label, isblank=isblank))
        # outgoing relations
        pred_obs = self._store.predicate_objects(iri)
        for pred, obj in pred_obs:
            obj_id = hash(obj)
            obj_label = obj.n3(self._store.namespace_manager)
            isliteral = isinstance(obj, Literal)
            isblank = isinstance(obj, BNode)
            self.nodes.add(
                Node(id=obj_id, label=obj_label, isliteral=isliteral, isblank=isblank)
            )
            pred_label = pred.n3(self._store.namespace_manager)
            self.edges.add(Edge(from_id=iri_id, to_id=obj_id, label=pred_label))
            if isblank:
                self._parse_instances(iri=obj)
        # incoming relations
        subj_preds = self._store.subject_predicates(iri)
        for subj, pred in subj_preds:
            subj_id = hash(subj)
            subj_label = subj.n3(self._store.namespace_manager)
            isliteral = isinstance(subj, Literal)
            isblank = isinstance(subj, BNode)
            self.nodes.add(
                Node(id=subj_id, label=subj_label, isliteral=isliteral, isblank=isblank)
            )
            pred_label = pred.n3(self._store.namespace_manager)
            self.edges.add(Edge(from_id=subj_id, to_id=iri_id, label=pred_label))

    def serialize(self) -> str:
        """serialize the parsed nodes and edges to JSON

        Intended to allow consumption of the diagram via API call.
        Only the neccessary attributes for rendering a diagram are returned.
        The consuming application is responsible for implementing the display logic.

        :returns: A JSON string of the form

            {
                "nodes": [...],
                "edges": [...]
            }

            where each node is a JSON serialization of a Node object and each edge is
            a serialization of an Edge object.
        """
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
        """render the parsed rdf as a diagram and display it.

        Provides some pre baked logic and templates for rendering the diagram
        in different formats. The rendered template is stored in a
        temporary file that will automatically be cleaned up by the OS
        after it has been closed.

        :param format: The format to use when rendering. Available formats are
            visjs, ...
        """
        if not self.serialization:
            self.serialize()
        if format == "visjs":
            render_visjs(self.serialization, self.overrides)
        elif format == "mermaid":
            render_mermaid(self.serialization, self.overrides)
        else:
            raise NotImplementedError
