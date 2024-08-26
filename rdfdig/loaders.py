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


def load_sparql(
    endpoint: str,
    iri: str,
    graph: str,
    username: str,
    password: str,
    limit: int = 1000,
    offset: int = 0,
):
    """load RDF from a remote SPARQL endpoint"""
    # TODO: handle retrieval of blank node properties
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
    g = Graph()
    while True:
        graph_query_part = f"from <{graph}>" if graph else ""
        iri_query_part = (
            f"values (?s ?o) {{(<{iri}> UNDEF) (UNDEF <{iri}>)}}" if iri else ""
        )
        query = f"""
        construct {{
         ?s ?p ?o
        }}
        {graph_query_part}
        where {{
            {iri_query_part}
            ?s ?p ?o
        }}
        limit {limit}
        offset {offset}
        """
        response = client.get(endpoint, headers=headers, params={"query": query})
        response.raise_for_status()
        g_part = Graph()
        g_part.parse(data=response.content, format="application/ld+json")
        g += g_part
        if len(g_part) < limit:
            break
        offset += limit
    return g
