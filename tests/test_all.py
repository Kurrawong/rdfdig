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


def test_class_serialization():
    """Test that all classes are retrieved from test data"""
    file = Path(__file__).parent / "data" / "edmond.ttl"
    diagram = Diagram()
    diagram.parse(source=file)
    nodes_edges_str = diagram.serialize()
    assert "schema:Person" in nodes_edges_str
    assert "schema:Organisation" in nodes_edges_str


def test_instance_serialization():
    """Test that all instances are retrieved from test data"""
    file = Path(__file__).parent / "data" / "edmond.ttl"
    diagram = Diagram()
    diagram.parse(source=file, iri="http://example.org/kurrawong")
    nodes_edges_str = diagram.serialize()
    assert "Edmond" in nodes_edges_str
    assert "Kurrawong AI" in nodes_edges_str


def test_prefix_expansion():
    """Test that a prefix can be expanded."""
    file = Path(__file__).parent / "data" / "lawson.ttl"
    diagram = Diagram()
    diagram.parse(source=file, iri="schema:Person")
