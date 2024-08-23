import json
import webbrowser
from pathlib import Path
from tempfile import NamedTemporaryFile

from jinja2 import Template


def render_visjs(serialization: dict, overrides: dict) -> None:
    default_color = {
        "border": "#2B7CE9",
        "background": "#D2E5FF",
    }
    bnode_color = {
        "border": "#D2E5FF",
        "background": "#606061",
    }
    options = {
        "edges": {
            "smooth": {"enabled": True, "type": "cubicBezier"},
            "arrows": {"to": {"enabled": True}},
        },
        "physics": {"enabled": True, "barnesHut": {"gravitationalConstant": -8000}},
    }
    for key, value in overrides.items():
        options[key] = value
    nodes = []
    for node in serialization["nodes"]:
        nodes.append(
            {
                "id": node["id"],
                "label": (
                    node["label"]
                    if len(node["label"]) < 45
                    else (node["label"][:45] + "...")
                ),
                "title": node["label"],
                "shape": "box" if node["isliteral"] else "dot",
                "color": bnode_color if node["isblank"] else default_color,
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
                "color": default_color,
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
