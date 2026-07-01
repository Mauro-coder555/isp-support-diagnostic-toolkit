import platform
import subprocess
from typing import Dict, Any, Optional


def ping_host(host: Optional[str]) -> Dict[str, Any]:
    """
    Runs a basic ping command against a host.
    Works on Windows and Linux/macOS.
    """
    if not host:
        return {
            "target": None,
            "status": "skipped",
            "message": "No host provided",
        }

    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "2", host]
    else:
        command = ["ping", "-c", "2", host]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=8,
        )

        if result.returncode == 0:
            return {
                "target": host,
                "status": "ok",
                "message": "Host responded to ping",
            }

        return {
            "target": host,
            "status": "failed",
            "message": "Host did not respond to ping",
        }

    except subprocess.TimeoutExpired:
        return {
            "target": host,
            "status": "timeout",
            "message": "Ping command timed out",
        }

    except Exception as error:
        return {
            "target": host,
            "status": "error",
            "message": str(error),
        }


def check_dns() -> Dict[str, Any]:
    """
    Runs a simple DNS/connectivity check using a public domain.
    """
    return ping_host("google.com")


def analyze_client_status(client: Dict[str, Any], gateway_check: Dict[str, Any], dns_check: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a simple support-oriented diagnosis based on client data
    and network checks.
    """
    findings = []
    possible_causes = []

    if client["service_status"] != "active":
        findings.append("Client service is not active")
        possible_causes.append("The service may be suspended or administratively blocked")

    if not client["assigned_ip"]:
        findings.append("Client has no assigned IP")
        possible_causes.append("The client may have an IP assignment issue")

    if client["radius_status"] != "authorized":
        findings.append("RADIUS status is not authorized")
        possible_causes.append("Authentication may be failing")

    if client["tr069_status"] != "online":
        findings.append("TR-069 status is not online")
        possible_causes.append("The customer router may be offline or not reporting")

    if client["has_open_ticket"]:
        findings.append("Client has an open support ticket")
        possible_causes.append("There may already be an active incident under review")

    if gateway_check["status"] != "ok":
        findings.append("Gateway did not respond correctly")
        possible_causes.append("There may be a local routing or network reachability issue")

    if dns_check["status"] != "ok":
        findings.append("DNS check failed")
        possible_causes.append("There may be a DNS or general connectivity issue")

    if not findings:
        findings.append("No obvious service issue detected")
        possible_causes.append("If the client still reports problems, check local WiFi, device configuration, or customer premises equipment")

    return {
        "findings": findings,
        "possible_causes": possible_causes,
    }