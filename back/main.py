#!/usr/bin/env python
"""CLI entry point para markdown-preview."""
import click

from .files.files import convert_file_to_md  # importa tu lógica
from .server import run


@click.command()
@click.argument("file_path", required=False, type=click.Path(exists=True))
@click.option("--run-server", "run_server", required=False, flag_value=True, type=click.BOOL)
def main(file_path: str, run_server: bool):
    """
    Convert any file to Markdown.

    Usage:
        mdp file.pdf               # Convert file to Markdown
        mdp --run-server           # Start local web server
        mdp file.docx --run-server # Error: cannot combine both

    If no file OR --run-server provided, shows error with help.
    """
    if run_server:
        run()
    elif file_path:
        content = convert_file_to_md(source=file_path)
        click.echo(f"Fin: {content}")
    else:
        click.echo("Ningún argumento proporcionado.\n")
        click.echo(main.get_help(click.Context(main)))


main()
