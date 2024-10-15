import getpass
import logging
from pathlib import Path

import httpx
from rdflib import Graph

logger = logging.getLogger(__name__)


def load_file(path: Path) -> Graph:
    """load RDF from path input format is automatically determined"""
    graph = Graph()
    logger.info(f"parsing rdf from {path.name}")
    graph.parse(path)
    return graph


def load_dir(path: Path, graph: Graph | None = None) -> Graph:
    """load RDF from files in path input format is automatically determined"""
    if graph is None:
        graph = Graph()
    for subpath in path.iterdir():
        if subpath.is_dir():
            load_dir(subpath, graph)
        else:
            logger.info(f"parsing rdf from {subpath.name}")
            graph.parse(subpath)
    return graph


def load_sparql(
    endpoint: str,
    iri: str | None,
    graph: str | None,
    username: str | None,
    password: str | None,
    limit: int = 1000,
    offset: int = 0,
    cutoff: int = 10000,
    timeout: int = 5,
):
    """load RDF from a remote SPARQL endpoint"""
    if username:
        if not password:
            password = getpass.getpass("password: ")
        auth = httpx.BasicAuth(username=username, password=password)
        client = httpx.Client(auth=auth, timeout=httpx.Timeout(timeout=timeout))
    else:
        client = httpx.Client(timeout=httpx.Timeout(timeout=timeout))
    g = Graph()
    if not iri:
        # first check how many triples there are
        headers = {
            "Content-Type": "application/sparql-query",
            "Accept": "application/json",
        }
        query = f"select (count(?s) as ?n) {f'from <{graph}>' if graph else ''} where {{?s ?p ?o}}"
        response = client.post(endpoint, headers=headers, data=query)
        if response.status_code == 405:
            response = client.get(endpoint, headers=headers, params={"query": query})
        response.raise_for_status()
        try:
            n_triples = int(response.json()["results"]["bindings"][0]["n"]["value"])
        except Exception as e:
            logging.error(
                f"could not count triples in remote endpoint. message: {e.args[0]}"
            )
            n_triples = 0
        if n_triples > cutoff:
            logger.warning(
                f"Warning remote dataset contains {n_triples:,} triples. Only the first {cutoff:,} will be fetched.\n"
                "This behaviour can be overriden by setting the 'cutoff' parameter."
            )
    while True:
        # fetch bnode properties to a depth of two
        query = f"""
        construct {{
         ?s ?p ?o .
         ?o ?p1 ?o1 .
         ?o1 ?p2 ?o2 .
        }}
        {f"from <{graph}>" if graph else ""}
        where {{
            {f"values (?s ?o) {{(<{iri}> UNDEF) (UNDEF <{iri}>)}}" if iri else ""}
            ?s ?p ?o .
            optional {{
                ?o ?p1 ?o1 .
                filter (isblank(?o))
                optional {{
                    ?o1 ?p2 ?o2 .
                    filter (isblank(?o1))
                }}
            }}
        }}
        limit {limit}
        offset {offset}
        """
        logger.debug(query)
        headers = {
            "Content-Type": "application/sparql-query",
            "Accept": "application/ld+json",
        }
        response = client.post(endpoint, headers=headers, data=query)
        if response.status_code == 405:
            response = client.get(endpoint, headers=headers, params={"query": query})
        response.raise_for_status()
        g_part = Graph()
        try:
            g_part.parse(data=response.content, format="application/ld+json")
        except Exception as e:
            logger.error(
                f"could not parse response from SPARQL endpoint.\nerror message: {e.args[0]}\nresponse content:\n{response.text}"
            )
        g += g_part
        if len(g_part) < limit:
            break
        offset += limit
        if offset > cutoff:
            break
    return g
