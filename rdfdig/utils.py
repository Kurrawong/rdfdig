from pathlib import Path
from textwrap import dedent

import toml
from rdflib import URIRef
from rdflib.namespace import NamespaceManager

pyproj_path = Path(__file__).parent.parent / "pyproject.toml"

# A list of supported output formats with a brief description of each
formats = {
    "visjs": dedent(
        """
    A JSON object containing an array of nodes and an array of edges.
    To be used with the https://visjs.org/ visualisation library.

        {
            "nodes": [{"id": 1, "label": "node 1"}, ...],
            "edges": [{"from": 1, "to": 2, "label": "uses"}, ...]
        }

    """
    ),
}
format_help_message = "The output format of the diagram.\n\n"
for format, description in formats.items():
    format_help_message += f"{format}{description}"


def get_version() -> str:
    """Extract the version number from pyproject.toml"""
    pyproj = toml.load(pyproj_path)
    return pyproj.get("tool", {}).get("poetry", {}).get("version", "")


def get_description() -> str:
    """Extract the project description from pyproject.toml"""
    pyproj = toml.load(pyproj_path)
    return pyproj.get("tool", {}).get("poetry", {}).get("description", "")


def expand_uri(iri: str, nm: NamespaceManager) -> URIRef:
    if iri.startswith("http"):
        return URIRef(iri)
    return URIRef(nm.expand_curie(iri))
