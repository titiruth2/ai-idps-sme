# Project summary

**AI-IDPS for SME networks** is a network intrusion detection and prevention system built around an unsupervised Isolation Forest model. It learns what normal traffic looks like on a small business network, flags connections that deviate, and blocks the most serious ones without waiting for an analyst.

## What it does

- Captures live traffic with Zeek, Scapy and Tshark and turns connection logs into features (originator bytes, responder bytes, duration, ports, protocol).
- Scores each connection with Isolation Forest and adds a DNS ensemble check.
- Ranks alerts as HIGH, MEDIUM or LOW by anomaly score and asset type.
- For HIGH alerts, adds an iptables DROP rule, ends the malicious session and writes a forensic log entry.
- Retrains in the background with a dual-model hot-swap, so detection never pauses.
- Shows alerts, topology and response actions on a Flask dashboard.

## Results on the VMware testbed

- Overall detection rate 83.2%, false positive rate 1.9%, F1 score 0.836.
- Mean time to detection about 10 seconds across four attack scenarios (Nmap SYN scan, Hydra SSH brute force, Metasploit vsftpd exploit, plus one more).
- Average per-packet latency 8.266 ms (95th percentile 12.056 ms).

## Where I'd like AI assistance

Hardening the feature pipeline, adding unit tests, and improving detection of slow-rate and fragmented scans.
