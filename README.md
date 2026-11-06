# ai-idps-sme

An AI-powered Intrusion Detection and Prevention System (AI-IDPS) for small and medium-sized enterprise (SME) networks. It captures live traffic, scores connections with an Isolation Forest model, prioritises alerts, and responds automatically to high-priority threats.

## Architecture

Six layers, from capture to response:

1. Live packet capture (Zeek, Scapy, Tshark)
2. Feature extraction
3. Isolation Forest detection engine with DNS ensemble detection
4. Alert correlation and priority classification (HIGH, MEDIUM, LOW)
5. Continuous hot-swap model retraining
6. Flask dashboard and automated response (iptables, session termination, forensic logging)

## Testbed

A VMware Workstation NAT network on a single laptop:

| Role | Machine | IP |
|---|---|---|
| IDS sensor | Kali Linux | 192.168.232.128 |
| Target server | Metasploitable | 192.168.232.129 |
| Manager PC | Windows 10 | 192.168.232.131 |
| Employee PC | Windows 7 | 192.168.232.132 |

## Stack

Python, scikit-learn (Isolation Forest), Zeek, Scapy, Tshark, Flask, iptables.

## Status

The source code is being added. Figure captions for the design and evaluation are in [docs/figures.md](docs/figures.md).
