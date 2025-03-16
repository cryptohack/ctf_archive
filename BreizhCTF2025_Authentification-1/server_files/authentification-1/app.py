from flask import Flask, render_template, request, redirect, url_for, make_response, send_from_directory
from crypto import build_token, verif_token
from gcm import BLOCK_LEN
import os

app = Flask(__name__)

FLAG = os.getenv("FLAG", "BZHCTF{default_flag}")
MASTER_KEY = os.urandom(BLOCK_LEN)
MAX_USERS  = 1 

users = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reset-db')
def reset_db():
    global MASTER_KEY
    global users

    MASTER_KEY = os.urandom(BLOCK_LEN)
    users = {}

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username]["password"] == password:
            token = build_token(MASTER_KEY, username, users[username]["role"])
            resp = make_response(redirect(url_for('admin')))
            resp.set_cookie('auth', token)

            return resp

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if len(users) >= MAX_USERS:
            return redirect(url_for('register')), 403

        username = request.form.get('username')
        password = request.form.get('password')

        if username not in users:
            users[username] = {
                "password": password,
                "role": "guest"
            }

            return redirect(url_for('login'))

    if len(users) >= MAX_USERS:
        return render_template('too_many_users.html'), 403
    else:
        return render_template('register.html')

@app.route('/admin')
def admin():
    auth_cookie = request.cookies.get('auth')

    try:
        if auth_cookie == None:
            msg = "Please login"
        elif verif_token(MASTER_KEY, auth_cookie) == True:
            msg = f"Well played! Here is your flag : {FLAG} !!!"
        else:
            msg = "You are not super_admin :("
    except:
        msg = "Error with the token..."

    return render_template("admin.html", msg=msg)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.png')

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=1337)

theme_colors = {
    'background': '#000000',
    'text': '#FFD700',
    'highlight': '#D40078',
    'button_bg': '#FFD700',
    'button_text': '#000000'
}

logo_url = "https://www.breizhctf.com/ims23/logo-prov2024.jpg"

