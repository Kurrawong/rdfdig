import getpass
from pathlib import Path

import httpx
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
    if username:
        if not password:
            password = getpass.getpass("password: ")
        auth = httpx.BasicAuth(username=username, password=password)
        client = httpx.Client(auth=auth)
    else:
        client = httpx.Client()
    headers = {
        "Content-Type": "application/sparql-query",
        "Accept": "application/ld+json",
    }
    # TODO: finish implementation
    query = """
    construct {
     ?s ?p ?o
    }
    """
    if graph:
        query += "from <%s>" % graph
    query += """
    where {
        ?s ?p ?o
    }
    limit 5
    """
    params = {"query": query}
    response = client.get(endpoint, headers=headers, params=params, auth=auth)
    response.raise_for_status()
    graph = Graph()
    graph.parse(data=response.content, format="application/ld+json")
    return graph
