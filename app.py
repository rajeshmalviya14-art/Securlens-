from flask import Flask, render_template_string, jsonify
from threading import Thread
import cv2
import numpy as np

app = Flask(__name__)

DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
<title>SecurLens</title>
<meta name="viewport" content="width=device-width">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0f1e;color:white;font-family:Arial}
.header{background:#111;padding:15px 20px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #00d4ff}
.logo{color:#00d4ff;font-size:22px;font-weight:bold}
.status{color:#00ff88;font-size:12px}
.cameras{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:15px}
.cam{background:#111;padding:12px;border-radius:8px;border:1px solid #333}
.cam.alert{border:2px solid red;background:#1a0000}
.cam-title{font-size:13px;font-weight:bold;margin-bottom:8px}
.cam-status{font-size:11px;padding:4px 8px;border-radius:4px;display:inline-block}
.cam-status.ok{background:#003300;color:#00ff88}
.cam-status.alert{background:#330000;color:red}
.btn{width:100%;padding:6px;margin-top:8px;border:none;border-radius:4px;cursor:pointer;font-size:11px}
.btn-alert{background:red;color:white}
.btn-ok{background:#222;color:#aaa;border:1px solid #333}
.history{margin:0 15px 15px;background:#111;border-radius:8px;padding:15px}
.history h3{color:#00d4ff;margin-bottom:10px}
.alert-item{background:#1a0000;padding:8px;border-radius:4px;margin-bottom:5px;font-size:12px;color:red}
</style>
</head>
<body>
<div class="header">
<div class="logo">🔐 SecurLens AI</div>
<div class="status">● LIVE</div>
</div>
<div class="cameras">
<div class="cam alert">
<div class="cam-title">CAM 1 - Main Gate</div>
<span class="cam-status alert">🚨 ALERT!</span>
<p style="font-size:11px;color:#aaa;margin-top:5px">Person - 97%</p>
<button class="btn btn-alert">LIVE DEKHO</button>
</div>
<div class="cam">
<div class="cam-title">CAM 2 - Shop</div>
<span class="cam-status ok">✅ Clear</span>
<p style="font-size:11px;color:#aaa;margin-top:5px">No Activity</p>
<button class="btn btn-ok">LIVE DEKHO</button>
</div>
<div class="cam">
<div class="cam-title">CAM 3 - Storage</div>
<span class="cam-status ok">✅ Clear</span>
<p style="font-size:11px;color:#aaa;margin-top:5px">No Activity</p>
<button class="btn btn-ok">LIVE DEKHO</button>
</div>
</div>
<div class="history">
<h3>📋 Alert History</h3>
<div class="alert-item">🚨 CAM 1 - Person Detected - 97% - 2:30 PM</div>
<div class="alert-item">🚨 CAM 1 - Motion - 85% - 1:15 PM</div>
</div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD)

@app.route('/api/status')
def status():
    return jsonify({"status": "online", "cameras": 3, "alerts": 2})

def run():
    app.run(host='0.0.0.0', port=5000, debug=False)

Thread(target=run, daemon=True).start()
print("SecurLens App Ready!")
print("Dashboard Live on port 5000!")
