"""Feature extraction from Zeek conn.log files."""
import pandas as pd

FEATURES = ["orig_bytes", "resp_bytes", "duration", "resp_port", "orig_port", "proto_num"]
PROTO_NUM = {"tcp": 6, "udp": 17, "icmp": 1}


def parse_conn_log(path):
    """Read a tab-separated Zeek conn.log into a DataFrame with model features."""
    fields = None
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("#fields"):
                fields = line.split("\t")[1:]
            elif line and not line.startswith("#"):
                rows.append(line.split("\t"))
    if fields is None:
        raise ValueError("No #fields header found: is this a Zeek conn.log?")
    df = pd.DataFrame(rows, columns=fields)
    return to_features(df)


def to_features(df):
    """Map Zeek columns to the six model features. '-' (unset) becomes 0."""
    num = lambda col: pd.to_numeric(df[col], errors="coerce").fillna(0)
    out = pd.DataFrame({
        "src_ip": df["id.orig_h"],
        "dst_ip": df["id.resp_h"],
        "orig_bytes": num("orig_bytes"),
        "resp_bytes": num("resp_bytes"),
        "duration": num("duration"),
        "resp_port": num("id.resp_p"),
        "orig_port": num("id.orig_p"),
        "proto_num": df["proto"].map(PROTO_NUM).fillna(0),
    })
    return out
