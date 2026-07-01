# Support flow

This project simulates a basic technical support workflow for an ISP operator.

## Goal

The goal is to help a support agent review a customer's service status, network information and possible causes of an issue from a single command-line tool.

## Basic flow

1. The operator receives a customer request.
2. The operator searches the customer by ID.
3. The tool retrieves customer data from MySQL.
4. The tool runs basic network checks.
5. The tool analyzes possible causes.
6. The tool generates a Markdown report.

## Current checks

- Service status
- Assigned IP
- Gateway reachability
- DNS reachability
- RADIUS status
- TR-069 status
- Open support ticket

## Example situations

### Suspended customer

If the service status is not active, the operator should check billing or administrative status before troubleshooting the network.

### No assigned IP

If the client has no assigned IP, the operator should review provisioning, IP assignment or DHCP-related records.

### RADIUS rejected

If RADIUS is not authorized, the issue may be related to authentication.

### TR-069 offline

If TR-069 is offline, the router may be disconnected, powered off, unreachable or not reporting correctly.

## Notes

This is a learning project. Some ISP concepts are simulated so the workflow can be practiced locally without real network infrastructure.