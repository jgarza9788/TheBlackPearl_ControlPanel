from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

# from flask_ngrok import run_with_ngrok

import time

import Config
SECRET_KEY = Config.Config().data["SECRET_KEY"]

import os
DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# run_with_ngrok(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DIR + '/instance/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

############################################
import subprocess

vpn_programs = [
    "openvpn-gui.exe",
    "openvpn.exe",
    "qbittorrent.exe",
    ]

def run_cmd(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def VPN_running():
    rc = run_cmd("tasklist")

    rc = str(rc.stdout.read())
    
    status = False

    for p in vpn_programs:
        if p in rc:
            status = True
    
    return status


VPN_ON = VPN_running()

def VPN_Text(vpnbool:bool) -> str:
    if vpnbool:
        return 'Running'
    else:
        return 'Is Off'


############################################


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##CREATE TABLE
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

with app.app_context():
    db.create_all()


############################################



############################################

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('controlpanel'))
    else:
        return redirect(url_for('login'))

    # if current_user.is_authenticated:
    #     return render_template(
    #         "controlpanel.html", 
    #         name=current_user.name, 
    #         logged_in=True,
    #         vpn_status=VPN_Text(VPN_ON)
    #         )
    # return render_template("index.html", logged_in=current_user.is_authenticated)


# @app.route('/register', methods=["GET", "POST"])
# def register():
#     if request.method == "POST":

#         if User.query.filter_by(email=request.form.get('email')).first():
#             #User already exists
#             flash("You've already signed up with that email, log in instead!")
#             return redirect(url_for('login'))

#         hash_and_salted_password = generate_password_hash(
#             request.form.get('password'),
#             method='pbkdf2:sha256',
#             salt_length=8
#         )
#         new_user = User(
#             email=request.form.get('email'),
#             name=request.form.get('name'),
#             password=hash_and_salted_password,
#         )
#         db.session.add(new_user)
#         db.session.commit()
#         login_user(new_user)
#         return redirect(url_for('index'))

#     return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
    
        user = User.query.filter_by(email=email).first()
        #Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('controlpanel'))
            # return redirect(url_for('home'))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route('/controlpanel')
@login_required
def controlpanel():
    print(current_user.name)
    return render_template(
        "controlpanel.html", 
        name=current_user.name, 
        logged_in=True,
        VPN_ON=VPN_ON
        )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/activateVPN')
@login_required
def activateVPN():
    os.startfile(r"C:\Users\JGarza\GitHub\VPNTools\activate_VPN_close.cmd")
    VPN_ON = True
    return render_template(
        "controlpanel.html", 
        name=current_user.name, 
        logged_in=True,
        VPN_ON=VPN_ON
        )

@app.route('/killVPN')
@login_required
def killVPN():
    os.startfile(r"C:\Users\JGarza\GitHub\VPNTools\kill_VPN_close.cmd")
    VPN_ON = False
    return render_template(
        "controlpanel.html", 
        name=current_user.name, 
        logged_in=True,
        VPN_ON=VPN_ON
        )

@app.route('/getVPNstatus')
@login_required
def getVPNstatus():
    VPN_ON = VPN_running()
    # time.sleep(5)
    return render_template(
        "controlpanel.html", 
        name=current_user.name, 
        logged_in=True,
        VPN_ON=VPN_ON
        )




if __name__ == "__main__":
    # app.run(debug=True, host= '192.168.1.254', port="8800")
    # app.run(debug=True,port="8800")
    # app.run(host='0.0.0.0',port=5000)
    # app.run(host='192.168.1.200',port="8800")
    # app.run(host='192.168.1.200',port="8800")
    # app.run(debug=False,host='0.0.0.0',port="8800")
    # app.run(host='0.0.0.0',port="8800",debug=False)
    # app.run(host='192.168.1.223',port="5000")
    # app.run(host='0.0.0.0',port="5000",debug=True)
    app.run(host='192.168.1.200',port="8800",debug=False)
    # app.run()