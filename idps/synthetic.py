"""Synthetic traffic for demos and tests. Not real captured data."""
import numpy as np
import pandas as pd

ATTACKER = "192.168.232.128"
SERVER = "192.168.232.129"
WORKSTATIONS = ["192.168.232.131", "192.168.232.132"]


def normal_traffic(n=2000, seed=0):
    rng = np.random.default_rng(seed)
    dst = rng.choice([SERVER] + WORKSTATIONS, size=n)
    return pd.DataFrame({
        "src_ip": rng.choice(WORKSTATIONS, size=n),
        "dst_ip": dst,
        "orig_bytes": rng.lognormal(6.5, 0.8, n),
        "resp_bytes": rng.lognormal(8.0, 1.0, n),
        "duration": rng.lognormal(0.0, 0.7, n),
        "resp_port": rng.choice([80, 443, 53, 445], size=n),
        "orig_port": rng.integers(49152, 65535, n),
        "proto_num": rng.choice([6, 17], size=n, p=[0.8, 0.2]),
    })


def port_scan(n=300, seed=1):
    """Many tiny, near-zero-duration connections to scattered ports (SYN scan shape)."""
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "src_ip": ATTACKER, "dst_ip": SERVER,
        "orig_bytes": rng.integers(0, 2, n).astype(float),
        "resp_bytes": np.zeros(n),
        "duration": rng.uniform(0, 0.01, n),
        "resp_port": rng.integers(1, 65535, n),
        "orig_port": rng.integers(40000, 60000, n),
        "proto_num": 6,
    })


def ssh_bruteforce(n=200, seed=2):
    """Repeated short SSH sessions with similar sizes."""
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "src_ip": ATTACKER, "dst_ip": SERVER,
        "orig_bytes": rng.normal(300, 30, n).clip(0),
        "resp_bytes": rng.normal(400, 40, n).clip(0),
        "duration": rng.uniform(0.05, 0.2, n),
        "resp_port": 22,
        "orig_port": rng.integers(40000, 60000, n),
        "proto_num": 6,
    })
