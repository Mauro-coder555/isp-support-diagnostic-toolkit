import argparse
from typing import Dict, Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from db import get_client_by_id
from network_checks import ping_host, check_dns, analyze_client_status
from report_generator import generate_report


console = Console()


def show_client_table(client: Dict[str, Any]) -> None:
    table = Table(title="Client information")

    table.add_column("Field", style="bold")
    table.add_column("Value")

    table.add_row("ID", str(client["id"]))
    table.add_row("Full name", str(client["full_name"]))
    table.add_row("Service plan", str(client["service_plan"]))
    table.add_row("Service status", str(client["service_status"]))
    table.add_row("Assigned IP", str(client["assigned_ip"] or "Not assigned"))
    table.add_row("Gateway IP", str(client["gateway_ip"] or "Not available"))
    table.add_row("Router brand", str(client["router_brand"] or "Not available"))
    table.add_row("Connection type", str(client["connection_type"] or "Not available"))
    table.add_row("RADIUS status", str(client["radius_status"] or "Unknown"))
    table.add_row("TR-069 status", str(client["tr069_status"] or "Unknown"))
    table.add_row("Last seen", str(client["last_seen"] or "Unknown"))
    table.add_row("Open ticket", "Yes" if client["has_open_ticket"] else "No")

    console.print(table)


def show_check_result(title: str, result: Dict[str, Any]) -> None:
    status = result["status"]

    if status == "ok":
        label = "[green]OK[/green]"
    elif status == "skipped":
        label = "[yellow]SKIPPED[/yellow]"
    else:
        label = "[red]FAILED[/red]"

    console.print(
        Panel(
            f"Target: {result['target']}\nStatus: {label}\nMessage: {result['message']}",
            title=title,
        )
    )


def show_diagnosis(diagnosis: Dict[str, Any]) -> None:
    console.print(Panel("\n".join(f"- {item}" for item in diagnosis["findings"]), title="Findings"))
    console.print(Panel("\n".join(f"- {item}" for item in diagnosis["possible_causes"]), title="Possible causes"))


def run_diagnosis(client_id: int) -> None:
    console.print(f"\n[bold]Searching client ID:[/bold] {client_id}\n")

    client = get_client_by_id(client_id)

    if not client:
        console.print(f"[red]Client with ID {client_id} was not found.[/red]")
        return

    show_client_table(client)

    console.print("\n[bold]Running network checks...[/bold]\n")

    gateway_check = ping_host(client["gateway_ip"])
    dns_check = check_dns()

    show_check_result("Gateway check", gateway_check)
    show_check_result("DNS check", dns_check)

    diagnosis = analyze_client_status(client, gateway_check, dns_check)
    show_diagnosis(diagnosis)

    report_path = generate_report(client, gateway_check, dns_check, diagnosis)

    console.print(f"\n[green]Report generated:[/green] {report_path}\n")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="ISP Support Diagnostic Toolkit"
    )

    parser.add_argument(
        "--client",
        type=int,
        required=True,
        help="Client ID to diagnose",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    run_diagnosis(args.client)