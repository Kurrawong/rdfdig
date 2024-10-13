import json
from pathlib import Path

import pytest

from rdfdig.core import Diagram


def test_file_loader():
    """Test that data can be loaded from a file."""
    file = Path(__file__).parent / "data" / "lawson.ttl"
    diagram = Diagram()
    diagram.parse(source=file)


def test_folder_loader():
    """Test that data can be loaded from a folder."""
    folder = Path(__file__).parent / "data"
    diagram = Diagram()
    diagram.parse(source=folder)


@pytest.mark.skip(reason="not implemented")
def test_sparql_loader():
    """Test that data can be loaded from a sparql endpoint."""
    assert True


def test_serialization():
    """Test that data can be serialized to JSON."""
    file = Path(__file__).parent / "data" / "lawson.ttl"
    diagram = Diagram()
    diagram.parse(source=file)
    nodes_edges_str = diagram.serialize()
    _ = json.loads(nodes_edges_str)


def test_prefix_expansion():
    """Test that a prefix can be expanded."""
    file = Path(__file__).parent / "data" / "lawson.ttl"
    diagram = Diagram()
    diagram.parse(source=file, iri="schema:Person")
