import argparse
from textwrap import dedent

from core import Diagram
from utils import format_help_message, formats, get_description, get_version

__version__ = get_version()
__description__ = get_description()


def main():
    parser = argparse.ArgumentParser(
        prog="rdfdig",
        description=__description__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    format_group = parser.add_argument_group("OUTPUT FORMATS")
    sparql_group = parser.add_argument_group("SPARQL OPTIONS")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "source",
        action="store",
        type=str,
        help="The data source. Can be SPARQL endpoint, file, or directory.",
    )
    parser.add_argument(
        "-i",
        "--iri",
        action="store",
        type=str,
        required=False,
        dest="iri",
        help=dedent(
            """
            An IRI, if specified, the diagram will show instance level
            connections for the resource specified by this argument.
            Otherwise the default class diagram will be shown.
        """
        ),
    )
    parser.add_argument(
        "-g",
        "--graph",
        action="store",
        type=str,
        required=False,
        dest="graph",
        help=dedent(
            """
            A named graph to limit the scope of the diagram. Can only be
            enforced if {source} is a SPARQL endpoint.
        """
        ),
    )
    parser.add_argument(
        "-r",
        "--render",
        action="store_true",
        default=False,
        dest="preview",
        help="render the diagram in the browser after serializing it.",
    )
    format_group.add_argument(
        "-f",
        "--format",
        action="store",
        choices=formats,
        default="visjs",
        dest="format",
        help=format_help_message,
    )
    sparql_group.add_argument(
        "-u",
        "--username",
        action="store",
        dest="username",
        help="username for HTTP Basic authentication. Only used if {source} is a SPARQL endpoint.",
    )
    sparql_group.add_argument(
        "-p",
        "--password",
        action="store",
        dest="password",
        help=dedent(
            """
            password for HTTP Basic authentication. if not provided then
            you will be prompted for one. Only used if {source} is a SPARQL
            endpoint and a username is supplied with the {--username} flag.
        """
        ),
    )
    args = parser.parse_args()
    diagram = Diagram()
    diagram.parse(args.source, args.iri, args.graph, args.username, args.password)
    print(diagram.serialize(format=args.format))
    if args.preview:
        diagram.render(format=args.format)


if __name__ == "__main__":
    main()
