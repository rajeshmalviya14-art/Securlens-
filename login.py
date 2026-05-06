from flask import Flask, render_template_string, request, redirect, session
import hashlib

app = Flask(__name__)
app.secret_key = "securlens2025"

USERS = {
    "demo@securlens.in": "demo123"
}

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>SecurLens - Login</title>
<meta name="viewport" content="width=device-width">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0f1e;display:flex;justify-content:center;align-items:center;height:100vh;font-family:Arial}
.box{background:#111;padding:40px;border-radius:12px;border:1px solid #00d4ff;width:320px}
.logo{color:#00d4ff;font-size:24px;font-weight:bold;text-align:center;margin-bottom:5px}
.tagline{color:#aaa;font-size:11px;text-align:center;margin-bottom:25px}
input{width:100%;padding:12px;margin:8px 0;background:#222;border:1px solid #333;color:white;border-radius:6px;font-size:14px}
.btn{width:100%;padding:12px;background:#00d4ff;border:none;border-radius:6px;color:#000;font-weight:bold;font-size:14px;cursor:pointer;margin-top:10px}
.tc{color:#aaa;font-size:10px;text-align:center;margin-top:15px}
.tc a{color:#00d4ff}
.error{color:red;font-size:12px;text-align:center;margin-top:10px}
</style>
</head>
<body>
<div class="box">
<div class="logo">🔐 SecurLens</div>
<div class="tagline">AI Camera Security Platform</div>
<form method="POST">
<input type="email" name="email" placeholder="Email Address" required>
<input type="password" name="password" placeholder="Password" required>
<button class="btn" type="submit">LOGIN</button>
</form>
<div class="tc">
By logging in you agree to our
<a href="/terms">Terms & Conditions</a>
</div>
{% if error %}
<div class="error">{{ error }}</div>
{% endif %}
</div>
</body>
</html>
"""

TERMS_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>SecurLens - Terms</title>
<style>
body{background:#0a0f1e;color:white;font-family:Arial;padding:20px}
.box{max-width:600px;margin:auto;background:#111;padding:30px;border-radius:12px}
h2{color:#00d4ff;margin-bottom:20px}
p{color:#aaa;margin-bottom:10px;font-size:13px;line-height:1.6}
.agree{display:block;width:100%;padding:12px;background:#00d4ff;border:none;border-radius:6px;color:#000;font-weight:bold;margin-top:20px;cursor:pointer;font-size:14px;text-align:center;text-decoration:none}
</style>
</head>
<body>
<div class="box">
<h2>SecurLens - Terms & Conditions</h2>
<p>1. SecurLens AI system is not 100% accurate.</p>
<p>2. SecurLens is not responsible for any theft or loss.</p>
<p>3. Price: Rs.50/camera/month + 18% GST.</p>
<p>4. Video stored locally on customer device only.</p>
<p>5. Cloud stores only alert clips as evidence.</p>
<p>6. Customer responsible for surveillance law compliance.</p>
<p>7. Data privacy: Camera footage not shared with anyone.</p>
<p>8. AI processes frames which are deleted immediately.</p>
<p>9. Service can be cancelled anytime.</p>
<a class="agree" href="/dashboard">I Agree - Continue</a>
</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in USERS and USERS[email] == password:
            session['user'] = email
            return redirect('/terms')
        error = "Invalid email or password!"
    return render_template_string(LOGIN_PAGE, error=error)

@app.route('/terms')
def terms():
    return render_template_string(TERMS_PAGE)

@app.route('/dashboard')
def dashboard():
    return redirect('/')

print("SecurLens Login System Ready!")
