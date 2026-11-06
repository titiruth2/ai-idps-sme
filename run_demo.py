"""Train on synthetic normal traffic, detect synthetic attacks, serve the dashboard.

    python run_demo.py            # http://127.0.0.1:5000
"""
import pandas as pd

from idps.dashboard import create_app
from idps.model import Detector
from idps.pipeline import detect
from idps.priority import SERVERS, WORKSTATIONS
from idps.synthetic import normal_traffic, port_scan, ssh_bruteforce

baseline = normal_traffic(2000)
detector = Detector(contamination=0.05).train(baseline)

live = pd.concat([normal_traffic(300, seed=9), port_scan(), ssh_bruteforce()], ignore_index=True)
# Limits recalibrated for this synthetic data; the defaults (-0.10 / -0.05 / 0.00) suit the original testbed.
tiers = [("HIGH", SERVERS, -0.04), ("MEDIUM", WORKSTATIONS, -0.02), ("LOW", None, 0.0)]
alerts = detect(detector, live, dry_run=True, tiers=tiers)
print(f"{len(alerts)} alerts from {len(live)} connections")

detector.retrain_async(pd.concat([baseline, normal_traffic(500, seed=5)])).join()
print("retraining:", detector.status())

create_app(detector, alerts).run(host="127.0.0.1", port=5000)
