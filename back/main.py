#!/usr/bin/env python
"""CLI entry point para markdown-preview."""
from pathlib import Path

import click

from .files.files import convert_file_to_md  # importa tu lógica

RUN = True


@click.command()
@click.argument("markdown_file", type=click.Path(exists=True))
def main(markdown_file: str):
    # Aquí llamas tu lógica existente:
    content = convert_file_to_md(source=markdown_file)
    click.echo(f"Fin: {content}")

main()
