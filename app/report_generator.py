from datetime import datetime
from pathlib import Path
from typing import Dict, Any


REPORTS_DIR = Path("reports")


def generate_report(
    client: Dict[str, Any],
    gateway_check: Dict[str, Any],
    dns_check: Dict[str, Any],
    diagnosis: Dict[str, Any],
) -> Path:
    """
    Generates a Markdown report with the support diagnosis.
    """
    REPORTS_DIR.mkdir(exist_ok=True)

    report_path = REPORTS_DIR / f"client_{client['id']}_report.md"

    content = f"""# ISP Support Diagnosis Report

Generated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Client information

- Client ID: {client["id"]}
- Full name: {client["full_name"]}
- Service plan: {client["service_plan"]}
- Service status: {client["service_status"]}
- Assigned IP: {client["assigned_ip"] or "Not assigned"}
- Gateway IP: {client["gateway_ip"] or "Not available"}
- Router brand: {client["router_brand"] or "Not available"}
- Connection type: {client["connection_type"] or "Not available"}
- RADIUS status: {client["radius_status"] or "Unknown"}
- TR-069 status: {client["tr069_status"] or "Unknown"}
- Last seen: {client["last_seen"] or "Unknown"}
- Has open ticket: {"Yes" if client["has_open_ticket"] else "No"}

## Network checks

### Gateway check

- Target: {gateway_check["target"]}
- Status: {gateway_check["status"]}
- Message: {gateway_check["message"]}

### DNS check

- Target: {dns_check["target"]}
- Status: {dns_check["status"]}
- Message: {dns_check["message"]}

## Findings

{format_list(diagnosis["findings"])}

## Possible causes

{format_list(diagnosis["possible_causes"])}

## Suggested next steps

{suggest_next_steps(client, gateway_check, dns_check)}
"""

    report_path.write_text(content, encoding="utf-8")
    return report_path


def format_list(items):
    return "\n".join(f"- {item}" for item in items)


def suggest_next_steps(client: Dict[str, Any], gateway_check: Dict[str, Any], dns_check: Dict[str, Any]) -> str:
    steps = []

    if client["service_status"] != "active":
        steps.append("Verify billing or administrative service status before deeper network troubleshooting.")

    if not client["assigned_ip"]:
        steps.append("Review IP assignment or DHCP/management system records.")

    if client["radius_status"] != "authorized":
        steps.append("Check RADIUS authentication logs and customer credentials.")

    if client["tr069_status"] != "online":
        steps.append("Check whether the router is powered on, reachable, or correctly provisioned.")

    if gateway_check["status"] != "ok":
        steps.append("Review gateway reachability, routing, or local network status.")

    if dns_check["status"] != "ok":
        steps.append("Check DNS resolution or upstream connectivity.")

    if not steps:
        steps.append("Ask the client for more details and verify local WiFi/device conditions.")

    return format_list(steps)