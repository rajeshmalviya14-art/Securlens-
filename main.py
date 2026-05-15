from flask import Flask, render_template_string, request, redirect, session
from supabase import create_client
from alert import send_call_alert, send_whatsapp_clip
import os

app = Flask(__name__)
app.secret_key = "securlens2025"

SUPABASE_URL = "https://cdunrmrornbisubrsnzi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNkdW5ybXJvcm5iaXN1YnJzbnppIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc5NjIxNTYsImV4cCI6MjA5MzUzODE1Nn0.3joKXdUQnBWZ1LJgVzF4lsbc6cgBKdkzOw2WR2LUWJY"
RAZORPAY_KEY_ID = "rzp_test_SpESekIywk3MST"

db = create_client(SUPABASE_URL, SUPABASE_KEY)

SIGNUP = """<!DOCTYPE html><html><head><title>SecurLens - Signup</title><meta name="viewport" content="width=device-width"><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0f1e;display:flex;justify-content:center;align-items:center;min-height:100vh;font-family:Arial}.box{background:#111;padding:40px;border-radius:12px;border:1px solid #00d4ff;width:320px;margin:20px}.logo{color:#00d4ff;font-size:24px;font-weight:bold;text-align:center;margin-bottom:5px}.tag{color:#aaa;font-size:11px;text-align:center;margin-bottom:20px}input{width:100%;padding:12px;margin:6px 0;background:#222;border:1px solid #333;color:white;border-radius:6px;font-size:13px}.btn{width:100%;padding:12px;background:#00d4ff;border:none;border-radius:6px;color:#000;font-weight:bold;font-size:14px;cursor:pointer;margin-top:10px}.link{color:#aaa;font-size:12px;text-align:center;margin-top:15px}.link a{color:#00d4ff}.tc{color:#aaa;font-size:10px;margin-top:10px}.error{color:red;font-size:12px;text-align:center;margin-top:10px}</style></head><body><div class="box"><div class="logo">🔐 SecurLens</div><div class="tag">AI Camera Security Platform</div><form method="POST"><input type="text" name="name" placeholder="Full Name" required><input type="email" name="email" placeholder="Email Address" required><input type="tel" name="phone" placeholder="Phone Number" required><input type="password" name="password" placeholder="Password" required><input type="number" name="cameras" placeholder="Number of Cameras" required><div class="tc"><input type="checkbox" name="agree" required> I agree to <a href="/terms">Terms & Conditions</a></div><button class="btn">CREATE ACCOUNT</button></form><div class="link">Already have account? <a href="/">Login</a></div>{% if error %}<div class="error">{{ error }}</div>{% endif %}</div></body></html>"""

LOGIN = """<!DOCTYPE html><html><head><title>SecurLens - Login</title><meta name="viewport" content="width=device-width"><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0f1e;display:flex;justify-content:center;align-items:center;height:100vh;font-family:Arial}.box{background:#111;padding:40px;border-radius:12px;border:1px solid #00d4ff;width:320px}.logo{color:#00d4ff;font-size:24px;font-weight:bold;text-align:center;margin-bottom:5px}.tag{color:#aaa;font-size:11px;text-align:center;margin-bottom:25px}input{width:100%;padding:12px;margin:8px 0;background:#222;border:1px solid #333;color:white;border-radius:6px;font-size:14px}.btn{width:100%;padding:12px;background:#00d4ff;border:none;border-radius:6px;color:#000;font-weight:bold;font-size:14px;cursor:pointer;margin-top:10px}.link{color:#aaa;font-size:12px;text-align:center;margin-top:15px}.link a{color:#00d4ff}.error{color:red;font-size:12px;text-align:center;margin-top:10px}</style></head><body><div class="box"><div class="logo">🔐 SecurLens</div><div class="tag">AI Camera Security Platform</div><form method="POST"><input type="email" name="email" placeholder="Email" required><input type="password" name="password" placeholder="Password" required><button class="btn">LOGIN</button></form><div class="link">New user? <a href="/signup">Create Account</a></div>{% if error %}<div class="error">{{ error }}</div>{% endif %}</div></body></html>"""

TERMS = """<!DOCTYPE html><html><head><title>SecurLens - Terms</title><meta name="viewport" content="width=device-width"><style>body{background:#0a0f1e;color:white;font-family:Arial;padding:20px}.box{max-width:600px;margin:auto;background:#111;padding:30px;border-radius:12px}h2{color:#00d4ff;margin-bottom:20px}p{color:#aaa;margin-bottom:10px;font-size:13px;line-height:1.6}.btn{display:block;width:100%;padding:12px;background:#00d4ff;border:none;border-radius:6px;color:#000;font-weight:bold;margin-top:20px;cursor:pointer;text-align:center;text-decoration:none}</style></head><body><div class="box"><h2>SecurLens - Terms & Conditions</h2><p>1. SecurLens AI system is not 100% accurate.</p><p>2. SecurLens is not responsible for any theft or loss.</p><p>3. Price: Rs.50/camera/month + 18% GST.</p><p>4. Video stored locally on customer device only.</p><p>5. Cloud stores only alert clips as evidence.</p><p>6. Customer responsible for surveillance law compliance.</p><p>7. Data privacy: Camera footage not shared with anyone.</p><p>8. AI processes frames deleted immediately after analysis.</p><p>9. Service can be cancelled anytime.</p><a class="btn" href="/signup">I Agree - Back to Signup</a></div></body></html>"""

PAYMENT = """<!DOCTYPE html><html><head><title>SecurLens - Payment</title><meta name="viewport" content="width=device-width"><script src="https://checkout.razorpay.com/v1/checkout.js"></script><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0f1e;display:flex;justify-content:center;align-items:center;height:100vh;font-family:Arial}.box{background:#111;padding:40px;border-radius:12px;border:1px solid #00d4ff;width:320px;text-align:center}.logo{color:#00d4ff;font-size:24px;font-weight:bold;margin-bottom:20px}h3{color:white;margin-bottom:10px}.price{color:#00d4ff;font-size:36px;font-weight:bold;margin:20px 0}.cameras{color:#aaa;font-size:14px;margin-bottom:20px}.btn{width:100%;padding:12px;background:#00d4ff;border:none;border-radius:6px;color:#000;font-weight:bold;font-size:16px;cursor:pointer}</style></head><body><div class="box"><div class="logo">🔐 SecurLens</div><h3>Complete Payment</h3><div class="price">₹{{ amount }}</div><div class="cameras">{{ cameras }} cameras × ₹50 + 18% GST</div><button class="btn" onclick="payNow()">PAY NOW</button></div><script>function payNow(){var options={key:"{{ key_id }}",amount:{{ amount_paise }},currency:"INR",name:"SecurLens",description:"AI Camera Surveillance",prefill:{name:"{{ name }}",email:"{{ email }}"},theme:{color:"#00d4ff"},handler:function(response){window.location.href="/payment-success?payment_id="+response.razorpay_payment_id;}};var rzp=new Razorpay(options);rzp.open();}</script></body></html>"""

DASHBOARD = """<!DOCTYPE html><html><head><title>SecurLens Dashboard</title><meta name="viewport" content="width=device-width"><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0f1e;color:white;font-family:Arial}.header{background:#111;padding:15px 20px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #00d4ff}.logo{color:#00d4ff;font-size:20px;font-weight:bold}.status{color:#00ff88;font-size:12px}.welcome{color:#aaa;font-size:12px;padding:10px 20px;background:#0d1a2e;display:flex;justify-content:space-between}.cameras{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:15px}.cam{background:#111;padding:12px;border-radius:8px;border:1px solid #333;transition:all 0.3s}.cam.alert{border:2px solid red;background:#1a0000}.cam-title{font-size:13px;font-weight:bold;margin-bottom:8px}.badge{font-size:11px;padding:4px 8px;border-radius:4px;display:inline-block}.badge.ok{background:#003300;color:#00ff88}.badge.alert{background:#330000;color:red}.btn{width:100%;padding:6px;margin-top:8px;border:none;border-radius:4px;cursor:pointer;font-size:11px;font-weight:bold}.btn-alert{background:red;color:white}.btn-ok{background:#222;color:#aaa;border:1px solid #333}.history{margin:0 15px 15px;background:#111;border-radius:8px;padding:15px;border:1px solid #333}.history h3{color:#00d4ff;margin-bottom:10px;font-size:14px}.alert-item{background:#1a0000;padding:8px;border-radius:4px;margin-bottom:5px;font-size:12px;color:red}.add-cam{margin:0 15px 15px;background:#111;border-radius:8px;padding:15px;border:1px solid #00d4ff}.add-cam h3{color:#00d4ff;margin-bottom:10px}.add-cam input{width:100%;padding:10px;margin:5px 0;background:#222;border:1px solid #333;color:white;border-radius:6px;font-size:13px}.add-cam button{width:100%;padding:10px;background:#00d4ff;border:none;border-radius:6px;color:#000;font-weight:bold;cursor:pointer;margin-top:5px}@keyframes pulse{0%{box-shadow:0 0 10px red}50%{box-shadow:0 0 30px red}100%{box-shadow:0 0 10px red}}.cam.alert.expanded{grid-column:span 2;animation:pulse 1s infinite}</style></head><body><div class="header"><div class="logo">🔐 SecurLens AI</div><div style="display:flex;gap:15px;align-items:center"><div class="status">● LIVE</div><a href="/logout" style="color:#ff4444;font-size:12px;text-decoration:none">Logout</a></div></div><div class="welcome"><span>Welcome, {{ name }}! | Cameras: {{ cameras }}</span><span style="color:{% if paid %}#00ff88{% else %}#ff4444{% endif %}">{% if paid %}✅ Active{% else %}⚠️ <a href="/payment" style="color:#ff4444">Pay Now</a>{% endif %}</span></div><div class="cameras" id="camGrid"><div class="cam alert" id="cam1"><div class="cam-title">CAM 1 - Main Gate</div><span class="badge alert">🚨 ALERT!</span><p style="font-size:11px;color:#aaa;margin-top:5px">Person - 97%</p><button class="btn btn-alert">LIVE DEKHO</button></div><div class="cam" id="cam2"><div class="cam-title">CAM 2 - Shop</div><span class="badge ok">✅ Clear</span><p style="font-size:11px;color:#aaa;margin-top:5px">No Activity</p><button class="btn btn-ok">LIVE DEKHO</button></div><div class="cam" id="cam3"><div class="cam-title">CAM 3 - Storage</div><span class="badge ok">✅ Clear</span><p style="font-size:11px;color:#aaa;margin-top:5px">No Activity</p><button class="btn btn-ok">LIVE DEKHO</button></div></div><div class="history"><h3>📋 Alert History</h3><div class="alert-item">🚨 CAM 1 - Person Detected - 97% - 2:30 PM</div><div class="alert-item">🚨 CAM 1 - Motion - 85% - 1:15 PM</div></div><div class="add-cam"><h3>➕ Add Camera</h3><form method="POST" action="/add-camera"><input type="text" name="cam_name" placeholder="Camera Name" required><input type="text" name="rtsp_url" placeholder="Camera RTSP URL" required><input type="text" name="location" placeholder="Location" required><button type="submit">ADD CAMERA</button></form></div><script>window.onload=function(){var c=document.getElementById('cam1');if(c){c.classList.add('expanded');var a=new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3');a.play().catch(function(){});}}</script></body></html>"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        result = db.table('users').select('*').eq('email', email).eq('password', password).execute()
        if result.data:
            user = result.data[0]
            session['user'] = email
            session['name'] = user['name']
            session['cameras'] = user['cameras']
            session['paid'] = user['paid']
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
        cameras = int(request.form.get('cameras', 1))
        agree = request.form.get('agree')
        if not agree:
            error = "Please agree to Terms & Conditions!"
        else:
            try:
                db.table('users').insert({'name': name, 'email': email, 'phone': phone, 'password': password, 'cameras': cameras, 'paid': False}).execute()
                session['user'] = email
                session['name'] = name
                session['cameras'] = cameras
                session['paid'] = False
                return redirect('/payment')
            except:
                error = "Email already registered!"
    return render_template_string(SIGNUP, error=error)

@app.route('/terms')
def terms():
    return render_template_string(TERMS)

@app.route('/payment')
def payment():
    if 'user' not in session:
        return redirect('/')
    cameras = int(session.get('cameras', 1))
    amount = cameras * 50
    gst = int(amount * 0.18)
    total = amount + gst
    return render_template_string(PAYMENT, amount=total, amount_paise=total*100, cameras=cameras, key_id=RAZORPAY_KEY_ID, name=session.get('name'), email=session.get('user'))

@app.route('/payment-success')
def payment_success():
    if 'user' not in session:
        return redirect('/')
    db.table('users').update({'paid': True}).eq('email', session['user']).execute()
    session['paid'] = True
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template_string(DASHBOARD, name=session.get('name'), cameras=session.get('cameras'), paid=session.get('paid', False))

@app.route('/add-camera', methods=['POST'])
def add_camera():
    if 'user' not in session:
        return redirect('/')
    cam_name = request.form.get('cam_name')
    rtsp_url = request.form.get('rtsp_url')
    location = request.form.get('location')
    db.table('cameras').insert({'customer_id': session['user'], 'camera_name': cam_name, 'rtsp_url': rtsp_url, 'location': location}).execute()
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
