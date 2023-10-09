from flask import Flask, render_template, request, jsonify, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
# from pymongo import MongoClient
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


# from flask_wtf import FlaskForm
# from wtforms import TextField, IntegerField, SubmitField

import shutil

from threading import Thread

import time,re
from fuzzywuzzy import fuzz

import Config
configdata = Config.Config().data
SECRET_KEY = configdata["SECRET_KEY"]

from drivedata import get_drivedata
from utils.IsRunning import is_running

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


# def VPN_running():
#     # return True
#     rc = run_cmd("tasklist")
#     rc = str(rc.stdout.read())
#     status = False
#     for p in vpn_programs:
#         if p in rc:
#             status = True
#     return status

# VPN_ON = VPN_running()

# def VPN_Text(vpnbool:bool) -> str:
#     if vpnbool:
#         return 'Running'
#     else:
#         return 'Is Off'


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

        drivedata = get_drivedata()

        # print(request.endpoint)
        return render_template(
            "home.html", 
            logged_in=current_user.is_authenticated,
            title=request.endpoint,
            drivedata=drivedata,
            programs=is_running(['NordVPN.exe','Plex Media Server.exe','qbittorrent.exe'])
            )
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
    # print(request.endpoint)

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
    
        user = User.query.filter_by(email=email).first()
        print(user)
        print(type(user))
        # user = db.users.find_one({'email': email})

        #Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.",'error')
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
        # elif not check_password_hash(user['password'], password):
            flash('Password incorrect, please try again.','error')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
            # return redirect(url_for('home'))

    return render_template(
        "login.html", 
        logged_in=current_user.is_authenticated,
        title=request.endpoint
        )

@app.route('/logout')
# @login_required
def logout():
    # print(request.endpoint)
    logout_user()
    return redirect(url_for('login'))

# @app.route('/controlpanel')
# @login_required
# def About():

#     if current_user.is_authenticated == False:
#         return redirect(url_for('login'))
    
#     return render_template(
#         "About.html", 
#         logged_in=current_user.is_authenticated,
#         title='\About'
#         )

MOVIE_LIST = []
SHOWS_LIST = []
TIMESTAMP = 0.0


def update_lists():
    '''
    updates the lists every hour
    '''
    global MOVIE_LIST
    global SHOWS_LIST
    global TIMESTAMP

    while 1==1:
        if (time.time() - TIMESTAMP) > 60*60*24: 
            print(time.time(),'updating lists')
            MOVIE_LIST = get_files(root=r'D:\Torrents\Movies',extensions=['mkv','avi','mp4'])
            if len(MOVIE_LIST) == 0:
                MOVIE_LIST += get_files(root=r'\\Theblackpearl\d\Torrents\Movies',extensions=['mkv','avi','mp4'])
            SHOWS_LIST = get_files(root=r'D:\Torrents\Shows',extensions=['mkv','mp4','avi'])
            if len(SHOWS_LIST) == 0:
                SHOWS_LIST += get_files(root=r'\\Theblackpearl\d\Torrents\Shows',extensions=['mkv','mp4','avi'])
            time.sleep(60) # every hour
            TIMESTAMP = time.time()
Thread(name='update_lists',target=update_lists,args=[]).start()

# MOVIES

# MOVIE_LIST = []
# MOVIE_TS = 0.0

# def get_movies():
#     global MOVIE_LIST
#     global MOVIE_TS

#     if (time.time() - MOVIE_TS) > 60*10:
#         MOVIE_LIST = get_files(root=r'D:\Torrents\Movies',extensions=['mkv','mp4'])
#         if len(MOVIE_LIST) == 0:
#             MOVIE_LIST += get_files(root=r'\\Theblackpearl\d\Torrents\Movies',extensions=['mkv','mp4'])
#         MOVIE_TS = time.time()
# get_movies()

@app.route('/movies')
@login_required
def movies():  
    global MOVIE_LIST
    global MOVIE_TS

    if current_user.is_authenticated == False:
        return redirect(url_for('login'))

    # get_movies()
    
    clear_cache()
    return render_template(
        "movies.html", 
        title=request.endpoint,
        logged_in=current_user.is_authenticated,
        item_list=MOVIE_LIST[0:25]
        )

@app.route("/movies/<query>", methods=['GET', 'POST'])
def movies_query(query):
    global MOVIE_LIST

    print(query)

    if len(query) < 2:
        return redirect(url_for("movies"))

    query = query.lower()

    filtered = []
    for i in MOVIE_LIST:
        if query in str(i).lower():
            filtered.append(i)
        else:
            temp = re.sub(r'[^A-Za-z]+',',',str(i).lower())
            for w in re.split(',',temp):
                # print(w)
                if fuzz.ratio(query, w) > 85:
                    filtered.append(i)
                    break;
    
    # return render_template("movies.html",portfolio_data=pl,query=query)
    return render_template(
        "movies.html", 
        title=request.endpoint,
        logged_in=current_user.is_authenticated,
        item_list=filtered
        )

# SHOWS 

# SHOWS_LIST = []
# SHOWS_TS = 0.0

# def get_shows():
#     global SHOWS_LIST
#     global SHOWS_TS
    
#     if (time.time() - SHOWS_TS) > 60*10:
#         SHOWS_LIST = get_files(root=r'D:\Torrents\Shows',extensions=['mkv','mp4'])
#         if len(SHOWS_LIST) == 0:
#             SHOWS_LIST += get_files(root=r'\\Theblackpearl\d\Torrents\Shows',extensions=['mkv','mp4'])
#         SHOWS_TS = time.time()
# get_shows()

@app.route('/shows')
@login_required
def shows():  
    global SHOWS_LIST
    global SHOWS_TS

    if current_user.is_authenticated == False:
        return redirect(url_for('login'))

    # get_shows()

    clear_cache()
    return render_template(
        "shows.html", 
        title=request.endpoint,
        logged_in=current_user.is_authenticated,
        item_list=SHOWS_LIST[0:25]
        )

@app.route("/shows/<query>", methods=['GET', 'POST'])
def shows_query(query):
    global SHOWS_LIST

    print(query)

    if len(query) < 2:
        return redirect(url_for("shows"))

    query = query.lower()

    filtered = []
    for i in SHOWS_LIST:
        if query in str(i).lower():
            filtered.append(i)
        else:
            temp = re.sub(r'[^A-Za-z]+',',',str(i).lower())
            for w in re.split(',',temp):
                # print(w)
                if fuzz.ratio(query, w) > 85:
                    filtered.append(i)
                    break;
    
    # return render_template("movies.html",portfolio_data=pl,query=query)
    return render_template(
        "shows.html", 
        title=request.endpoint,
        logged_in=current_user.is_authenticated,
        item_list=filtered
        )

# COMICS


@app.route('/download/<fullpath>',methods=['GET'])
@login_required
def download(fullpath):  
    fullpath = fullpath.strip().strip('\n')
    print(fullpath)  

    if current_user.is_authenticated == False:
        return redirect(url_for('login'))

    file = fullpath.split('\\')[-1]

    flash('preparing file ...')
    path = os.path.join(DIR,'static','cache',file)
    shutil.copy2(fullpath,path)

    flash('starting download')

    # return send_from_directory(app.config['ROOT_FOLDER'],path)
    return send_from_directory('static\cache',file, as_attachment=True)


@app.route('/movieroulette')
@login_required
def Movie_Roulette():  
    global MOVIE_LIST

    if current_user.is_authenticated == False:
        return redirect(url_for('login'))

    import random
    rc = []
    while len(rc) == 0:
        rc.append(random.choice(MOVIE_LIST))
    
    clear_cache()
    return render_template(
        "movieroulette.html", 
        title=request.endpoint,
        logged_in=current_user.is_authenticated,
        item_list=rc
        )

## VPN #
# @app.route('/NordVPN')
# @login_required
# def NordVPN():       
#     if current_user.is_authenticated == False:
#         return redirect(url_for('login'))
    
#     # VPN_ON = VPN_running()
#     VPN_ON = True

#     return render_template(
#         "NordVPN.html", 
#         title=request.endpoint,
#         logged_in=current_user.is_authenticated,
#         VPN_ON=VPN_ON
#         )

# # @app.route('/activateVPN')
# @app.route('/activateVPN',methods=['POST'])
# @login_required
# def activateVPN():
#     if current_user.is_authenticated == False:
#         return redirect(url_for('login'))
    
#     os.startfile(r"C:\Users\JGarza\GitHub\VPNTools\activate_VPN_close.cmd")

#     VPN_ON = VPN_running()
#     # return redirect(url_for('VPN'))
#     return jsonify({'result':'Successful','VPN_ON':VPN_ON})


# # @app.route('/killVPN')
# @app.route('/killVPN',methods=['POST'])
# @login_required
# def killVPN():
#     if current_user.is_authenticated == False:
#         return redirect(url_for('login'))
    
#     os.startfile(r"C:\Users\JGarza\GitHub\VPNTools\kill_VPN_close.cmd")

#     VPN_ON = VPN_running()
#     # return redirect(url_for('VPN'))
#     return jsonify({'result':'Successful','VPN_ON':VPN_ON})


# @app.route('/getVPNstatus',methods=['POST'])
# # @app.route('/getVPNstatus')
# @login_required
# def getVPNstatus():
#     if current_user.is_authenticated == False:
#         return redirect(url_for('login'))
#     # LOCS.append(request.endpoint)
#     VPN_ON = VPN_running()
#     # return redirect(url_for('VPN'))
#     return jsonify({'result':'Successful','VPN_ON':VPN_ON})



from math import sin, cos, acos

@app.context_processor
def utility_processor():
    return dict(cos=cos, sin=sin, acos=acos)


if __name__ == "__main__":

    # app.run()
    app.run(host='0.0.0.0',port="5000",debug=True)
    # app.run(host='0.0.0.0',port="8800",debug=False)


    
    