"""`contract-lens` CLI — flag the clauses worth attention in a contract / ToS.

    contract-lens review --file terms.txt
    contract-lens demo
"""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from .client import LLMClient
from .config import Settings
from .reviewer import Reviewer

app = typer.Typer(add_completion=False, help="AI contract / ToS reviewer — flags risky clauses (not legal advice).")
console = Console()

_EXAMPLE = (
    "SUBSCRIPTION TERMS. 1. Term. This agreement renews automatically for successive 12-month "
    "periods unless you give written notice at least 90 days before the end of the current term. "
    "2. Fees. We may increase fees at any time at our sole discretion, effective immediately. "
    "3. Liability. Our total liability shall not exceed £50 in aggregate. You agree to indemnify us "
    "against all claims. 4. IP. Any feedback or content you provide becomes our exclusive property. "
    "5. Data. We may use, share and sell your usage data to third parties. 6. Changes. We may modify "
    "these terms at any time; continued use constitutes acceptance. 7. Disputes. You waive any right "
    "to a jury trial or to participate in a class action."
)

_SEV = {"high": "red", "medium": "yellow", "low": "dim"}


def _print(result) -> None:
    r = result.review
    style = {"high": "red", "medium": "yellow", "low": "green"}.get(r.overall_risk, "cyan")
    console.print(Panel(f"[bold]Overall risk: {r.overall_risk.upper()}[/]\n{r.summary}", title="Contract review", border_style=style))
    for f in r.findings:
        console.print(f"\n[{_SEV.get(f.severity.value,'white')}]{f.severity.value.upper()}[/] · [cyan]{f.clause_type}[/]")
        console.print(f"  {f.concern}")
        console.print(f"  [green]→[/] {f.recommendation}")
        console.print(f"  [dim]“{f.quote}”[/]")
    console.print(f"\n[dim]{result.disclaimer}[/]")


def _run(text: str) -> None:
    settings = Settings.from_env()
    with console.status("Reviewing…"):
        result = Reviewer(LLMClient(settings)).review(text)
    _print(result)


@app.callback()
def _root() -> None:
    """AI contract / ToS reviewer (educational, not legal advice)."""


@app.command()
def review(
    file: Path = typer.Option(None, "--file", help="Path to the contract / ToS text."),
    text: str = typer.Option(None, "--text", help="Inline contract text."),
) -> None:
    if file:
        _run(file.read_text(encoding="utf-8"))
    elif text:
        _run(text)
    else:
        console.print("[red]Provide --file or --text (or run `contract-lens demo`).[/]")
        raise typer.Exit(1)


@app.command()
def demo() -> None:
    """Review a baked-in intentionally one-sided subscription contract."""
    _run(_EXAMPLE)


if __name__ == "__main__":
    app()
