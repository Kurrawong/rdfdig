from pathlib import Path

from rdflib import Graph


def load_file(path: Path) -> Graph:
    """load RDF from path input format is automatically determined"""
    graph = Graph()
    graph.parse(path)
    return graph


def load_dir(path: Path) -> Graph:
    """load RDF from files in path input format is automatically determined"""
    graph = Graph()
    for file in path.iterdir():
        graph.parse(file)
    return graph


def load_sparql(endpoint: str, iri: str, graph: str, username: str, password: str):
    """load RDF from a remote SPARQL endpoint"""
    # TODO: implement this
    raise NotImplementedError
