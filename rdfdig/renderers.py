import json
import webbrowser
from pathlib import Path
from tempfile import NamedTemporaryFile

from jinja2 import Template


def render_visjs(serialization: str, options: dict) -> None:
    default_options = {
        "edges": {
            "smooth": {"enabled": True, "type": "cubicBezier"},
        },
        "physics": {
            "enabled": True,
        },
    }
    for key, value in options.items():
        default_options[key] = value
    data = json.loads(serialization)
    template_path = Path(__file__).parent / "templates" / "visjs.html"
    template = Template(template_path.read_text())
    tempfile = NamedTemporaryFile(mode="w", suffix=".html", delete=False)
    tempfile.write(
        template.render(
            nodes=json.dumps(data["nodes"]),
            edges=json.dumps(data["edges"]),
            options=json.dumps(default_options),
        )
    )
    tempfile.close()
    webbrowser.open_new_tab(f"file:///{tempfile.name}")
    return
