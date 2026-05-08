from flask import Flask, render_template_string, request, redirect, session

app = Flask(__name__)
app.secret_key = "securlens2025"

USERS = {"demo@securlens.in": "demo123"}

LOGIN_PAGE = """<!DOCTYPE html><html><head><title>SecurLens - Login</title><meta name="viewport" content="width=device-width"><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0f1e;display:flex;justify-content:center;align-items:center;height:100vh;font-family:Arial}.box{background:#111;padding:40px;border-radius:12px;border:1px solid #00d4ff;width:320px}.logo{color:#00d4ff;font-size:24px;font-weight:bold;text-align:center;margin-bottom:5px}.tag{color:#aaa;font-size:11px;text-align:center;margin-bottom:25px}input{width:100%;padding:12px;margin:8px 0;background:#222;border:1px solid #333;color:white;border-radius:6px;font-size:14px}.btn{width:100%;padding:12px;background:#00d4ff;border:none;border-radius:6px;color:#000;font-weight:bold;font-size:14px;cursor:pointer;margin-top:10px}.error{color:red;font-size:12px;text-align:center;margin-top:10px}</style></head><body><div class="box"><div class="logo">🔐 SecurLens</div><div class="tag">AI Camera Security Platform</div><form method="POST"><input type="email" name="email" placeholder="Email" required><input type="password" name="password" placeholder="Password" required><button class="btn">LOGIN</button></form>{% if error %}<div class="error">{{ error }}</div>{% endif %}</div></body></html>"""

DASHBOARD = """<!DOCTYPE html><html><head><title>SecurLens Dashboard</title><meta name="viewport" content="width=device-width"><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0f1e;color:white;font-family:Arial}.header{background:#111;padding:15px 20px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #00d4ff}.logo{color:#00d4ff;font-size:20px;font-weight:bold}.status{color:#00ff88;font-size:12px}.cameras{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:15px}.cam{background:#111;padding:12px;border-radius:8px;border:1px solid #333}.cam.alert{border:2px solid red;background:#1a0000}.cam-title{font-size:13px;font-weight:bold;margin-bottom:8px}.badge{font-size:11px;padding:4px 8px;border-radius:4px;display:inline-block}.badge.ok{background:#003300;color:#00ff88}.badge.alert{background:#330000;color:red}.btn{width:100%;padding:6px;margin-top:8px;border:none;border-radius:4px;cursor:pointer;font-size:11px;font-weight:bold}.btn-alert{background:red;color:white}.btn-ok{background:#222;color:#aaa;border:1px solid #333}.history{margin:0 15px 15px;background:#111;border-radius:8px;padding:15px;border:1px solid #333}.history h3{color:#00d4ff;margin-bottom:10px;font-size:14px}.alert-item{background:#1a0000;padding:8px;border-radius:4px;margin-bottom:5px;font-size:12px;color:red}</style></head><body><div class="header"><div class="logo">🔐 SecurLens AI</div><div class="status">● LIVE</div></div><div class="cameras"><div class="cam alert"><div class="cam-title">CAM 1 - Main Gate</div><span class="badge alert">🚨 ALERT!</span><p style="font-size:11px;color:#aaa;margin-top:5px">Person - 97%</p><button class="btn btn-alert">LIVE DEKHO</button></div><div class="cam"><div class="cam-title">CAM 2 - Shop</div><span class="badge ok">✅ Clear</span><p style="font-size:11px;color:#aaa;margin-top:5px">No Activity</p><button class="btn btn-ok">LIVE DEKHO</button></div><div class="cam"><div class="cam-title">CAM 3 - Storage</div><span class="badge ok">✅ Clear</span><p style="font-size:11px;color:#aaa;margin-top:5px">No Activity</p><button class="btn btn-ok">LIVE DEKHO</button></div></div><div class="history"><h3>📋 Alert History</h3><div class="alert-item">🚨 CAM 1 - Person Detected - 97% - 2:30 PM</div><div class="alert-item">🚨 CAM 1 - Motion - 85% - 1:15 PM</div></div></body></html>"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in USERS and USERS[email] == password:
            session['user'] = email
            return redirect('/dashboard')
        error = "Invalid email or password!"
    return render_template_string(LOGIN_PAGE, error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template_string(DASHBOARD)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
