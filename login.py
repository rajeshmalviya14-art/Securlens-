from flask import Flask, render_template_string, request, redirect, session
app = Flask(__name__)
app.secret_key = "securlens2025"
USERS = {"demo@securlens.in": "demo123"}
LOGIN_PAGE = """<!DOCTYPE html><html><head><title>SecurLens</title><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0f1e;display:flex;justify-content:center;align-items:center;height:100vh;font-family:Arial}.box{background:#111;padding:40px;border-radius:12px;border:1px solid #00d4ff;width:320px}.logo{color:#00d4ff;font-size:24px;font-weight:bold;text-align:center;margin-bottom:20px}input{width:100%;padding:12px;margin:8px 0;background:#222;border:1px solid #333;color:white;border-radius:6px}.btn{width:100%;padding:12px;background:#00d4ff;border:none;border-radius:6px;color:#000;font-weight:bold;cursor:pointer;margin-top:10px}.error{color:red;font-size:12px;text-align:center;margin-top:10px}</style></head><body><div class="box"><div class="logo">🔐 SecurLens</div><form method="POST"><input type="email" name="email" placeholder="Email" required><input type="password" name="password" placeholder="Password" required><button class="btn">LOGIN</button></form>{% if error %}<div class="error">{{ error }}</div>{% endif %}</div></body></html>"""
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
    return "<h1 style='color:white;background:#0a0f1e;padding:20px'>SecurLens Dashboard - Coming Soon!</h1>"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
