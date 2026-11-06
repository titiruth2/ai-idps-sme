"""Score traffic and turn anomalies into prioritised alerts."""
from .priority import TIERS, classify
from .response import respond


def detect(detector, df, dry_run=True, log_path="forensic.log", tiers=TIERS):
    df = df.copy()
    df["score"] = detector.scores(df)
    alerts = []
    for row in df.itertuples():
        tier = classify(row.score, row.dst_ip, tiers)
        if tier is None:
            continue
        alert = {"src_ip": row.src_ip, "dst_ip": row.dst_ip, "resp_port": int(row.resp_port),
                 "score": round(float(row.score), 4), "priority": tier}
        alert["actions"] = respond(alert, dry_run, log_path)
        alerts.append(alert)
    return alerts
