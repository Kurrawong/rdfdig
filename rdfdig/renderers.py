import html
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


def render_mermaid(serialization: dict, overrides: dict) -> None:
    options = {}
    for key, value in overrides:
        options[key] = value
    mermaid = """
    %%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%
    flowchart LR
        classDef default fill:#efefef,stroke:#808080
        classDef bnode fill:#ffffff,stroke:#808080
        classDef literal fill:#ffffff,stroke:#808080
    """

    def id_str(id: int) -> str:
        if id > 0:
            return "A" + str(id)
        return "B" + str(id)[1:]

    for node in serialization["nodes"]:
        node_id = id_str(node["id"])
        label = html.escape(node["label"]).replace("&quot;", "#quot;")
        if node["isblank"]:
            mermaid += f"""
            {node_id}(("bnode"))
            class {node_id} bnode
            """
        elif node["isliteral"]:
            mermaid += f"""
            {node_id}["{label}"]
            class {node_id} literal
            """
        else:
            mermaid += f"""
            {node_id}("{label}")
            class {node_id} default
            """
    for edge in serialization["edges"]:
        from_id = id_str(edge["from"])
        to_id = id_str(edge["to"])
        label = html.escape(edge["label"])
        mermaid += f"""
        {from_id} -->|"{label}"|{to_id}
        """
    template_path = Path(__file__).parent / "templates" / "mermaid.html"
    template = Template(template_path.read_text())
    tempfile = NamedTemporaryFile(mode="w", suffix=".html", delete=False)
    tempfile.write(template.render(mermaid=mermaid))
    tempfile.close()
    webbrowser.open_new_tab(f"file:///{tempfile.name}")
    return
