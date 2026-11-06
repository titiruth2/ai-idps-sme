"""Flask dashboard and JSON API."""
from collections import Counter

from flask import Flask, jsonify, render_template_string

PAGE = """<!doctype html><title>AI-IDPS</title>
<body style="font-family:sans-serif;max-width:900px;margin:2rem auto">
<h2>AI-IDPS dashboard</h2><div id=s></div>
<table border=1 cellpadding=6 id=t><tr><th>Priority<th>Source<th>Target<th>Port<th>Score</table>
<script>
async function load(){
 const st=await (await fetch('/api/stats')).json();
 s.textContent=`Alerts: ${st.total} | HIGH ${st.HIGH} | MEDIUM ${st.MEDIUM} | LOW ${st.LOW}`;
 const a=await (await fetch('/api/alerts')).json();
 for(const x of a.slice(-50).reverse()){
  t.insertAdjacentHTML('beforeend',`<tr><td>${x.priority}<td>${x.src_ip}<td>${x.dst_ip}<td>${x.resp_port}<td>${x.score}`)}
}
load();
</script></body>"""


def create_app(detector, alerts):
    """alerts is a list shared with the detection loop."""
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template_string(PAGE)

    @app.get("/api/alerts")
    def api_alerts():
        return jsonify(alerts)

    @app.get("/api/stats")
    def api_stats():
        c = Counter(a["priority"] for a in alerts)
        return jsonify({"total": len(alerts), "HIGH": c["HIGH"], "MEDIUM": c["MEDIUM"], "LOW": c["LOW"]})

    @app.get("/api/retraining-status")
    def api_retraining():
        return jsonify(detector.status())

    return app
