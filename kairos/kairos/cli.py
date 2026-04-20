"""Kairos CLI — corre agentes individuales del pipeline."""

from __future__ import annotations

import json
import sys

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from kairos.agents import KeywordResearcher
from kairos.clients import get_client
from kairos.schemas import KeywordResearchInput

load_dotenv()
console = Console()


@click.group()
def cli():
    """Kairos — SEO Content-as-a-Service pipeline."""


@cli.command()
@click.option("--domain", required=True, help="Client domain (e.g., acme.com)")
@click.option("--topic", required=True, help="Seed topic for the cluster")
@click.option("--audience", required=True, help="Target audience description")
@click.option("--client-id", default="demo", help="Internal client identifier")
@click.option("--real-data", is_flag=True, help="Use real DataForSEO (default: mock)")
@click.option("--output", type=click.Choice(["pretty", "json"]), default="pretty")
def research(domain, topic, audience, client_id, real_data, output):
    """Run the Keyword Researcher agent on a seed topic."""
    try:
        data_client = get_client(use_mock=not real_data)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        sys.exit(1)

    researcher = KeywordResearcher(data_client=data_client)
    input_data = KeywordResearchInput(
        client_id=client_id,
        domain=domain,
        seed_topic=topic,
        target_audience=audience,
    )

    with console.status("[bold cyan]Researching keywords..."):
        cluster = researcher.research(input_data)

    if output == "json":
        click.echo(cluster.model_dump_json(indent=2))
        return

    console.print(f"\n[bold cyan]Cluster:[/bold cyan] {cluster.cluster_name}\n")
    console.print(
        f"[bold green]Primary:[/bold green] {cluster.primary_keyword.keyword} "
        f"(vol={cluster.primary_keyword.search_volume}, "
        f"KD={cluster.primary_keyword.keyword_difficulty}, "
        f"intent={cluster.primary_keyword.intent})\n"
    )

    table = Table(title="Secondary keywords", show_lines=False)
    table.add_column("Keyword", style="yellow")
    table.add_column("Volume", justify="right")
    table.add_column("KD", justify="right")
    table.add_column("Intent")
    for kw in cluster.secondary_keywords:
        table.add_row(
            kw.keyword,
            str(kw.search_volume or "-"),
            str(kw.keyword_difficulty or "-"),
            kw.intent,
        )
    console.print(table)

    console.print("\n[bold]People Also Ask:[/bold]")
    for q in cluster.paa_questions:
        console.print(f"  • {q}")

    console.print("\n[bold]Competitors:[/bold]")
    for url in cluster.competitor_urls:
        console.print(f"  • {url}")

    console.print(f"\n[bold]Content gap:[/bold] {cluster.content_gap_notes}")
    console.print(f"[bold]Angle:[/bold] [italic]{cluster.recommended_angle}[/italic]\n")


if __name__ == "__main__":
    cli()
