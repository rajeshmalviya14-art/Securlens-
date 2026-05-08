from flask import Flask, render_template_string, request, redirect, session
import hashlib, os

app = Flask(__name__)
app.secret_key = "securlens2025"

USERS = {}

SIGNUP = """<!DOCTYPE html><html><head><title>SecurLens - Signup</title><meta name="viewport" content="width=device-width"><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0f1e;display:flex;justify-content:center;align-items:center;min-height:100vh;font-family:Arial}.box{background:#111;padding:40px;border-radius:12px;border:1px solid #00d4ff;width:320px;margin:20px}.logo{color:#00d4ff;font-size:24px;font-weight:bold;text-align:center;margin-bottom:5px}.tag{color:#aaa;font-size:11px;text-align:center;margin-bottom:20px}input{width:100%;padding:12px;margin:6px 0;background:#222;border:1px solid #333;color:white;border-radius:6px;font-size:13px}.btn{width:100%;padding:12px;background:#00d4ff;border:none;border-radius:6px;color:#000;font-weight:bold;font-size:14px;cursor:pointer;margin-top:10px}.link{color:#00d4ff;font-size:12px;text-align:center;margin-top:15px}.link a{color:#00d4ff}.tc{color:#aaa;font-size:10px;margin-top:10px}.error{color:red;font-size:12px;text-align:center;margin-top:10px}</style></head><body><div class="box"><div class="logo">🔐 SecurLens</div><div class="tag">AI Camera Security Platform</div><form method="POST"><input type="text" name="name" placeholder="Full Name" required><input type="email" name="email" placeholder="Email Address" required><input type="tel" name="phone" placeholder="Phone Number" required><input type="password" name="password" placeholder="Password" required><input type="number" name="cameras" placeholder="Number of Cameras" required><div class="tc"><input type="checkbox" name="agree" required> I agree to <a href="/terms">Terms & Conditions</a></div><button class="btn">CREATE ACCOUNT</button></form><div class="link">Already have account? <a href="/">Login</a></div>{% if error %}<div class="error">{{ error }}</div>{% endif %}</div></body></html>"""

LOGIN = """<!DOCTYPE html><html><head><title>SecurLens - Login</title><meta name="viewport" content="width=device-width"><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0f1e;display:flex;justify-content:center;align-items:center;height:100vh;font-family:Arial}.box{background:#111;padding:40px;border-radius:12px;border:1px solid #00d4ff;width:320px}.logo{color:#00d4ff;font-size:24px;font-weight:bold;text-align:center;margin-bottom:5px}.tag{color:#aaa;font-size:11px;text-align:center;margin-bottom:25px}input{width:100%;padding:12px;margin:8px 0;background:#222;border:1px solid #333;color:white;border-radius:6px;font-size:14px}.btn{width:100%;padding:12px;background:#00d4ff;border:none;border-radius:6px;color:#000;font-weight:bold;font-size:14px;cursor:pointer;margin-top:10px}.link{color:#aaa;font-size:12px;text-align:center;margin-top:15px}.link a{color:#00d4ff}.error{color:red;font-size:12px;text-align:center;margin-top:10px}</style></head><body><div class="box"><div class="logo">🔐 SecurLens</div><div class="tag">AI Camera Security Platform</div><form method="POST"><input type="email" name="email" placeholder="Email" required><input type="password" name="password" placeholder="Password" required><button class="btn">LOGIN</button></form><div class="link">New user? <a href="/signup">Create Account</a></div>{% if error %}<div class="error">{{ error }}</div>{% endif %}</div></body></html>"""

TERMS = """<!DOCTYPE html><html><head><title>SecurLens - Terms</title><meta name="viewport" content="width=device-width"><style>body{background:#0a0f1e;color:white;font-family:Arial;padding:20px}.box{max-width:600px;margin:auto;background:#111;padding:30px;border-radius:12px}h2{color:#00d4ff;margin-bottom:20px}p{color:#aaa;margin-bottom:10px;font-size:13px;line-height:1.6}.btn{display:block;width:100%;padding:12px;background:#00d4ff;border:none;border-radius:6px;color:#000;font-weight:bold;margin-top:20px;cursor:pointer;text-align:center;text-decoration:none}</style></head><body><div class="box"><h2>🔐 SecurLens - Terms & Conditions</h2><p>1. SecurLens AI system is not 100% accurate.</p><p>2. SecurLens is not responsible for any theft or loss.</p><p>3. Price: ₹50/camera/month + 18% GST.</p><p>4. Video stored locally on customer device only.</p><p>5. Cloud stores only alert clips as evidence.</p><p>6. Customer responsible for surveillance law compliance.</p><p>7. Data privacy: Camera footage not shared with anyone.</p><p>8. AI processes frames deleted immediately after analysis.</p><p>9. Service can be cancelled anytime.</p><a class="btn" href="/signup">I Agree - Back to Signup</a></div></body></html>"""

DASHBOARD = """<!DOCTYPE html><html><head><title>SecurLens Dashboard</title><meta name="viewport" content="width=device-width"><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0f1e;color:white;font-family:Arial}.header{background:#111;padding:15px 20px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #00d4ff}.logo{color:#00d4ff;font-size:20px;font-weight:bold}.status{color:#00ff88;font-size:12px}.welcome{color:#aaa;font-size:12px;padding:10px 20px;background:#0d1a2e}.cameras{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:15px}.cam{background:#111;padding:12px;border-radius:8px;border:1px solid #333}.cam.alert{border:2px solid red;background:#1a0000}.cam-title{font-size:13px;font-weight:bold;margin-bottom:8px}.badge{font-size:11px;padding:4px 8px;border-radius:4px;display:inline-block}.badge.ok{background:#003300;color:#00ff88}.badge.alert{background:#330000;color:red}.btn{width:100%;padding:6px;margin-top:8px;border:none;border-radius:4px;cursor:pointer;font-size:11px;font-weight:bold}.btn-alert{background:red;color:white}.btn-ok{background:#222;color:#aaa;border:1px solid #333}.history{margin:0 15px 15px;background:#111;border-radius:8px;padding:15px;border:1px solid #333}.history h3{color:#00d4ff;margin-bottom:10px;font-size:14px}.alert-item{background:#1a0000;padding:8px;border-radius:4px;margin-bottom:5px;font-size:12px;color:red}.add-cam{margin:0 15px 15px;background:#111;border-radius:8px;padding:15px;border:1px solid #00d4ff}.add-cam h3{color:#00d4ff;margin-bottom:10px}.add-cam input{width:100%;padding:10px;margin:5px 0;background:#222;border:1px solid #333;color:white;border-radius:6px;font-size:13px}.add-cam button{width:100%;padding:10px;background:#00d4ff;border:none;border-radius:6px;color:#000;font-weight:bold;cursor:pointer;margin-top:5px}</style></head><body><div class="header"><div class="logo">🔐 SecurLens AI</div><div style="display:flex;gap:15px;align-items:center"><div class="status">● LIVE</div><a href="/logout" style="color:#ff4444;font-size:12px;text-decoration:none">Logout</a></div></div><div class="welcome">Welcome, {{ name }}! | Cameras: {{ cameras }}</div><div class="cameras"><div class="cam alert"><div class="cam-title">CAM 1 - Main Gate</div><span class="badge alert">🚨 ALERT!</span><p style="font-size:11px;color:#aaa;margin-top:5px">Person - 97%</p><button class="btn btn-alert">LIVE DEKHO</button></div><div class="cam"><div class="cam-title">CAM 2 - Shop</div><span class="badge ok">✅ Clear</span><p style="font-size:11px;color:#aaa;margin-top:5px">No Activity</p><button class="btn btn-ok">LIVE DEKHO</button></div><div class="cam"><div class="cam-title">CAM 3 - Storage</div><span class="badge ok">✅ Clear</span><p style="font-size:11px;color:#aaa;margin-top:5px">No Activity</p><button class="btn btn-ok">LIVE DEKHO</button></div></div><div class="history"><h3>📋 Alert History</h3><div class="alert-item">🚨 CAM 1 - Person Detected - 97% - 2:30 PM</div><div class="alert-item">🚨 CAM 1 - Motion - 85% - 1:15 PM</div></div><div class="add-cam"><h3>➕ Add Camera</h3><form method="POST" action="/add-camera"><input type="text" name="cam_name" placeholder="Camera Name (e.g. Main Gate)" required><input type="text" name="rtsp_url" placeholder="Camera RTSP URL" required><input type="text" name="location" placeholder="Location" required><button type="submit">ADD CAMERA</button></form></div></body></html>"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in USERS and USERS[email]['password'] == password:
            session['user'] = email
            session['name'] = USERS[email]['name']
            session['cameras'] = USERS[email]['cameras']
            return redirect('/dashboard')
        error = "Invalid email or password!"
    return render_template_string(LOGIN, error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        cameras = request.form.get('cameras')
        agree = request.form.get('agree')
        if not agree:
            error = "Please agree to Terms & Conditions!"
        elif email in USERS:
            error = "Email already registered!"
        else:
            USERS[email] = {'name': name, 'phone': phone, 'password': password, 'cameras': cameras}
            session['user'] = email
            session['name'] = name
            session['cameras'] = cameras
            return redirect('/dashboard')
    return render_template_string(SIGNUP, error=error)

@app.route('/terms')
def terms():
    return render_template_string(TERMS)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template_string(DASHBOARD, name=session.get('name'), cameras=session.get('cameras'))

@app.route('/add-camera', methods=['POST'])
def add_camera():
    if 'user' not in session:
        return redirect('/')
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
