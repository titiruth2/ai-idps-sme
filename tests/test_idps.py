import pandas as pd

from idps.model import Detector
from idps.pipeline import detect
from idps.priority import classify
from idps.synthetic import normal_traffic, port_scan, ssh_bruteforce


def make():
    return Detector(0.05).train(normal_traffic(2000))


def test_priority_tiers():
    assert classify(-0.12, "192.168.232.129") == "HIGH"
    assert classify(-0.12, "192.168.232.131") == "MEDIUM"
    assert classify(-0.07, "192.168.232.129") == "LOW"
    assert classify(0.05, "192.168.232.129") is None


def test_detects_most_scan_traffic(tmp_path):
    d = make()
    alerts = detect(d, port_scan(), log_path=str(tmp_path / "f.log"))
    assert len(alerts) > 0.9 * 300


def test_normal_traffic_false_positive_rate_is_low(tmp_path):
    d = make()
    alerts = detect(d, normal_traffic(1000, seed=77), log_path=str(tmp_path / "f.log"))
    assert len(alerts) < 0.15 * 1000


def test_dry_run_never_executes(tmp_path):
    d = make()
    tiers = [("HIGH", None, 0.0)]
    alerts = detect(d, port_scan(), dry_run=True, log_path=str(tmp_path / "f.log"), tiers=tiers)
    assert alerts and alerts[0]["priority"] == "HIGH" and alerts[0]["actions"]
    for a in alerts:
        assert all(not act["executed"] for act in a["actions"])


def test_hot_swap_increments_and_keeps_scoring():
    d = make()
    t = d.retrain_async(normal_traffic(1000, seed=3))
    d.scores(normal_traffic(10))          # scoring works while retraining
    t.join()
    assert d.status()["total_swaps"] == 1
    assert d.status()["retraining"] is False
