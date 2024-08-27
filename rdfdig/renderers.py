import json
import webbrowser
from pathlib import Path
from tempfile import NamedTemporaryFile

from jinja2 import Template


def render_visjs(serialization: dict, overrides: dict) -> None:
    """render the serialization of a Diagram instance using visjs

    The rendered template is written to a temp file and opened in
    the default web browser.
    """
    options = {
        "edges": {
            "color": {
                "border": "#808080",
                "background": "#efefef",
                "highlight": "#9DBDFF",
            },
            "smooth": {"enabled": True, "type": "cubicBezier"},
            "arrows": {"to": {"enabled": True}},
        },
        "physics": {"enabled": True, "barnesHut": {"gravitationalConstant": -8000}},
        "groups": {
            "default": {
                "color": {
                    "border": "#808080",
                    "background": "#efefef",
                    "highlight": "#9DBDFF",
                },
                "shape": "box",
                "margin": 16,
                "widthConstraint": {"minimum": 100, "maximum": 100},
                "heightConstraint": {"minimum": 50, "maximum": 50},
            },
            "literal": {
                "color": {
                    "border": "#808080",
                    "background": "#ffffff",
                    "highlight": "#9DBDFF",
                },
                "shape": "box",
                "widthConstraint": {"minimum": 100},
                "heightConstraint": {"minimum": 25, "maximum": 25},
            },
            "bnode": {
                "color": {
                    "border": "#808080",
                    "background": "#ffffff",
                    "highlight": "#9DBDFF",
                },
                "shape": "dot",
                "widthConstraint": {"minimum": 100},
            },
        },
    }
    for key, value in overrides.items():
        options[key] = value
    nodes = []
    for node in serialization["nodes"]:
        if node["isblank"]:
            group = "bnode"
        elif node["isliteral"]:
            group = "literal"
        else:
            group = "default"
        nodes.append(
            {
                "id": node["id"],
                "label": (
                    node["label"]
                    if len(node["label"]) < 45
                    else (node["label"][:45] + "...")
                ),
                "title": node["label"],
                "group": group,
            }
        )
    edges = []
    pairs = {}
    for edge in serialization["edges"]:
        pair = hash(edge["from"]) + hash(edge["to"])
        title, width = pairs.get(pair, ("", 1))
        if title:
            title += "\n"
        title += edge["label"]
        width += 0.5
        edges.append(
            {
                "from": edge["from"],
                "to": edge["to"],
                "title": title,
                "physics": {"enabled": False},
                "width": width,
            }
        )
        pairs[pair] = (title, width)
    template_path = Path(__file__).parent / "templates" / "visjs.html"
    template = Template(template_path.read_text())
    tempfile = NamedTemporaryFile(mode="w", suffix=".html", delete=False)
    tempfile.write(
        template.render(
            nodes=json.dumps(nodes),
            edges=json.dumps(edges),
            options=json.dumps(options),
        )
    )
    tempfile.close()
    webbrowser.open_new_tab(f"file:///{tempfile.name}")
    return
