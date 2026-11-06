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

## Quick start

```bash
pip install -r requirements.txt pytest
python -m pytest -q
python run_demo.py        # trains on synthetic traffic, detects scans, serves http://127.0.0.1:5000
```

## Layout

| Path | Purpose |
|---|---|
| `idps/features.py` | Parse Zeek `conn.log` into the six model features |
| `idps/model.py` | Isolation Forest detector with dual-model hot-swap retraining |
| `idps/priority.py` | HIGH / MEDIUM / LOW tiering by score and asset type |
| `idps/response.py` | iptables block, session kill, forensic log (dry-run by default) |
| `idps/pipeline.py` | Score traffic and produce prioritised alerts |
| `idps/dashboard.py` | Flask dashboard and JSON API (`/api/alerts`, `/api/stats`, `/api/retraining-status`) |
| `idps/synthetic.py` | Synthetic normal and attack traffic for demos and tests |

## Status and honesty note

This repository is a clean **rebuild** of the system described in the dissertation. The original testbed scripts were not available when this was written, so the code here has not produced the dissertation's reported results (83.2% detection, 1.9% false positive rate). The demo uses synthetic traffic, and the score thresholds in `idps/priority.py` are the dissertation's design values; recalibrate them on your own traffic. Live capture with Zeek, Scapy and Tshark is not wired in yet: `parse_conn_log` reads a Zeek log you produce yourself.

Automated response runs in dry-run mode unless you pass `dry_run=False`, which executes `iptables` and needs root. Only run it on a lab network you own.

Figure captions are in [docs/figures.md](docs/figures.md).
