"""Alert priority tiering from anomaly score and asset type.

Default limits come from the dissertation design. Score ranges depend on the training data,
so recalibrate them (pass `tiers`) for a new environment.
"""

SERVERS = {"192.168.232.129"}
WORKSTATIONS = {"192.168.232.131", "192.168.232.132"}

# (tier, asset set or None for all assets, score must be below)
TIERS = [
    ("HIGH", SERVERS, -0.10),
    ("MEDIUM", WORKSTATIONS, -0.05),
    ("LOW", None, 0.0),
]


def classify(score, dst_ip, tiers=TIERS):
    """Return HIGH, MEDIUM, LOW, or None when the score is not anomalous."""
    for tier, assets, limit in tiers:
        if score < limit and (assets is None or dst_ip in assets):
            return tier
    return None
