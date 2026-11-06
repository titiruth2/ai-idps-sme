"""Automated response for HIGH alerts. Dry-run by default: nothing touches the firewall unless enabled."""
import datetime
import json
import subprocess


def block_ip(ip, dry_run=True):
    cmd = ["iptables", "-I", "INPUT", "-s", ip, "-j", "DROP"]
    if dry_run:
        return {"action": "block_ip", "ip": ip, "executed": False, "cmd": " ".join(cmd)}
    subprocess.run(cmd, check=True)
    return {"action": "block_ip", "ip": ip, "executed": True, "cmd": " ".join(cmd)}


def kill_session(src_ip, dst_ip, dry_run=True):
    cmd = ["conntrack", "-D", "-s", src_ip, "-d", dst_ip]
    if dry_run:
        return {"action": "kill_session", "executed": False, "cmd": " ".join(cmd)}
    subprocess.run(cmd, check=False)
    return {"action": "kill_session", "executed": True, "cmd": " ".join(cmd)}


def forensic_log(alert, path="forensic.log"):
    entry = {"time": datetime.datetime.now().isoformat(timespec="seconds"), **alert}
    with open(path, "a") as fh:
        fh.write(json.dumps(entry) + "\n")
    return entry


def respond(alert, dry_run=True, log_path="forensic.log"):
    """HIGH: block, end session, log. Anything else: log only."""
    actions = []
    if alert["priority"] == "HIGH":
        actions.append(block_ip(alert["src_ip"], dry_run))
        actions.append(kill_session(alert["src_ip"], alert["dst_ip"], dry_run))
    forensic_log({**alert, "actions": actions}, log_path)
    return actions
