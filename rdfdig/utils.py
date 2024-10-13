from pathlib import Path

from rdflib import URIRef
from rdflib.namespace import NamespaceManager

pyproj_path = Path(__file__).parent.parent / "pyproject.toml"

# A list of supported renderer formats
formats = {
    "visjs": "Interactive diagram using visjs.org",
    "mermaid": "A mermaid diagram, using mermaid.js.org",
}
format_help_message = "The output format of the diagram.\n"
for format, description in formats.items():
    format_help_message += f"\n{format}: {description}"


def expand_uri(iri: str, nm: NamespaceManager) -> URIRef:
    """Safely expand a prefixed IRI

    uses the given namespace manager to resolve prefixes

    :param iri: the iri to expand
    :returns: a URIRef of the expanded iri
    :raises: ValueError if the iri cannot be expanded
    """
    if iri.startswith("http"):
        return URIRef(iri)
    return URIRef(nm.expand_curie(iri))
