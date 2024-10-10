import json
from pathlib import Path

import pytest

from rdfdig.core import Diagram


def test_file_loader():
    file = Path(__file__).parent / "data" / "lawson.ttl"
    diagram = Diagram()
    diagram.parse(source=file)


def test_folder_loader():
    folder = Path(__file__).parent / "data"
    diagram = Diagram()
    diagram.parse(source=folder)


@pytest.mark.skip(reason="not implemented")
def test_sparql_loader():
    assert True


def test_serialization():
    file = Path(__file__).parent / "data" / "lawson.ttl"
    diagram = Diagram()
    diagram.parse(source=file)
    nodes_edges_str = diagram.serialize()
    _ = json.loads(nodes_edges_str)


def test_prefix_expansion():
    file = Path(__file__).parent / "data" / "lawson.ttl"
    diagram = Diagram()
    diagram.parse(source=file, iri="schema:Person")
