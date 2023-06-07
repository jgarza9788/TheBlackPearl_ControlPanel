from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
# from pymongo import MongoClient
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

# from flask_wtf import FlaskForm
# from wtforms import TextField, IntegerField, SubmitField

import shutil

import time,re
from fuzzywuzzy import fuzz

import Config
configdata = Config.Config().data
SECRET_KEY = configdata["SECRET_KEY"]

import os
DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)



app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DIR + '/instance/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# app.config.update(dict(SECRET_KEY=SECRET_KEY))
# client = MongoClient('localhost:27017') 
# db = client.TBP


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
    # return True

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
# def load_user(user):
#     return db.users.find_one({'email': user['email']})

# class User(FlaskForm):
#     email = TextField('email')
#     password = TextField('password')
#     create = SubmitField('Login')

##CREATE TABLE
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

with app.app_context():
    db.create_all()


############################################


def get_files(root:str='D:\\',extensions:list=[]) -> list:
    print('get_files')
    result = []
    for path, directories, files in os.walk(root):
        for file in files:
            for e in extensions:
                if file.startswith('.'):
                    continue
                if file.endswith(e):
                    result.append({
                        # 'id': len(result),
                        'fullpath': os.path.join(path, file),
                        'file': file
                    })
                continue
    return result


ITEMS = []
ITEMSTIME = 0.0
def get_items():
    global ITEMS
    global ITEMSTIME

    if (time.time() - ITEMSTIME) > 3600:
        ITEMS = get_files(root=r'D:\Torrents\Movies',extensions=['mkv','mp4'])
        ITEMS += get_files(root=r'D:\Torrents\Shows',extensions=['mkv','mp4'])

        if len(ITEMS) == 0:
            ITEMS += get_files(root=r'\\Theblackpearl\d\Torrents\Movies',extensions=['mkv','mp4'])
            ITEMS += get_files(root=r'\\Theblackpearl\d\Torrents\Shows',extensions=['mkv','mp4']) 

        ITEMSTIME = time.time()
    
    return ITEMS

# items = get_items()

############################################


def clear_cache():
    static_cache = os.path.join(DIR,'static','cache')
    listdir = os.listdir(static_cache)
    if len(listdir) > 10:
        for i in os.listdir(static_cache):
            try:
                os.remove(os.path.join(static_cache,i))
            except:
                pass

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
#         return redirect(url_for('controlpanel'))

#     return render_template("register.html", logged_in=current_user.is_authenticated)



@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
    
        user = User.query.filter_by(email=email).first()
        print(user)
        print(type(user))
        # user = db.users.find_one({'email': email})

        #Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
        # elif not check_password_hash(user['password'], password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('controlpanel'))
            # return redirect(url_for('home'))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/controlpanel')
@login_required
def controlpanel():

    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    
    return render_template(
        "controlpanel.html", 
        email=current_user.email.replace('@',''), #don't pass in @
        logged_in=True,
        VPN_ON=VPN_ON
        )


# files0 #

@app.route('/ITEMS')
@login_required
def ITEMS():  

    if current_user.is_authenticated == False:
        return redirect(url_for('login'))

    items = get_items()

    clear_cache()
    return render_template(
        "ITEM_LIST.html", 
        name=current_user.name, 
        logged_in=True,
        title = 'ITEMS',
        category='ITEMS',
        item_list = items[0:25]
        )

@app.route("/ITEMSQ/<query>", methods=['GET', 'POST'])
@login_required
def ITEMS_QUERY(query):

    if current_user.is_authenticated == False:
        return redirect(url_for('login'))

    print(query)

    if len(query) < 2:
        return redirect(url_for("ITEMS"))

    query = query.lower()

    pl = []
    for i in get_items():
        if query in str(i).lower():
            pl.append(i)
        else:
            temp = re.sub(r'[^A-Za-z]+',',',str(i).lower())
            for w in re.split(',',temp):
                # print(w)
                if fuzz.ratio(query, w) > 85:
                    pl.append(i)
                    break;
    
    # return render_template("portfolio.html",portfolio_data=pl,query=query)
    return render_template(
        "ITEM_LIST.html", 
        name=current_user.name, 
        logged_in=True,
        title = 'Query',
        category='ITEMS',
        item_list = pl
        )

@app.route('/<category>/<fullpath>')
@login_required
def ITEM(category,fullpath):  

    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
  
    print(category,fullpath)
    return render_template(
        "ITEM.html", 
        name=current_user.name, 
        logged_in=True,
        category = category,
        item = fullpath
        )

@app.route('/download/<fullpath>')
@login_required
def download(fullpath):    
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))

    file = fullpath.split('\\')[-1]

    flash('preparing file ...')
    path = os.path.join(DIR,'static','cache',file)
    shutil.copy2(fullpath,path)

    flash('starting download')

    # return send_from_directory(app.config['ROOT_FOLDER'],path)
    return send_from_directory('static\cache',file, as_attachment=True)

# VPN #

@app.route('/VPN')
@login_required
def VPN():    
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    
    VPN_ON = VPN_running()

    return render_template(
        "VPN.html", 
        name=current_user.name, 
        logged_in=True,
        VPN_ON=VPN_ON
        )

@app.route('/activateVPN')
@login_required
def activateVPN():
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    
    os.startfile(r"C:\Users\JGarza\GitHub\VPNTools\activate_VPN_close.cmd")
    return redirect(url_for('VPN'))

@app.route('/killVPN')
@login_required
def killVPN():
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    
    os.startfile(r"C:\Users\JGarza\GitHub\VPNTools\kill_VPN_close.cmd")
    return redirect(url_for('VPN'))

@app.route('/getVPNstatus')
@login_required
def getVPNstatus():
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    
    return redirect(url_for('VPN'))


from math import sin, cos, acos

@app.context_processor
def utility_processor():
    return dict(cos=cos, sin=sin, acos=acos)

if __name__ == "__main__":

    # app.run()
    # app.run(host='0.0.0.0',port="5000",debug=True)
    app.run(host='0.0.0.0',port="8800",debug=False)
    
    