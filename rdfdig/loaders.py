from pathlib import Path

from rdflib import Graph


def load_file(path: Path) -> Graph:
    graph = Graph()
    graph.parse(path)
    return graph


def load_dir(path: Path) -> Graph:
    graph = Graph()
    for file in path.iterdir():
        graph.parse(file)
    return graph


def load_sparql(endpoint: str, iri: str, graph: str, username: str, password: str):
    # TODO: implement this
    raise NotImplementedError()
