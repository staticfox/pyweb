#!/usr/bin/env python3.5
import flask_login
import sys
import traceback
import yaml

from gamesurge.decorators import access, requiresrvx
from gamesurge.utils import Services
from flask import Flask, flash, render_template, request, g
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('etc/config.py')
app.config['GS_CONF'] = None
db = SQLAlchemy(app)

""" Session management """
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

def check_config():
    try:
        app.config['GS_CONF'] = yaml.load(open('./etc/config.yaml', 'r'))
    except yaml.YAMLError:
        print("Error reading YAML file: {}".format(traceback.format_exc()), file=sys.stderr, flush=True)
        exit(1)
    except FileNotFoundError:
        print('You must setup your config file in "etc/config.yaml"', file=sys.stderr, flush=True)
        exit(1)

    if 'qserver' not in app.config['GS_CONF']:
        print("You must supply a valid config file.", file=sys.stderr, flush=True)
        exit(1)

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

""" Not implemented yet """
def notImplemented():
    return "This is not implemented"

""" Login via SrvX """
@app.route('/login', methods=['GET', 'POST'])
@requiresrvx(app)
def login():
    if request.method == 'GET':
        return render_template('login.html')

    f = request.form

    """ Missing account/password field """
    if not f['account'] or not f['password']:
        flash('You must supply a username and password', 'error')
        return render_template('login.html')

    """ Login success """
    if g.services.check_login(f['account'], f['password']):
        flash('You have been logged in.', 'success')
        return render_template('index.html')

    """ Login failed """
    flash('Username or password incorrect', 'error')
    return render_template('login.html', status=2)

@app.route('/staff')
@access(100)
def staff():
    return notImplemented()

@app.route('/logout')
def logout():
    return notImplemented()

""" Ensure the SrvX connection is closed,
    even if a page raises an exception
"""
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'services'):
        g.services.srvx.disconnect()

""" Staff accounts only """
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    access = db.Column(db.Integer)

    def __init__(self, username, access):
        self.username = username
        self.access = access

    def __repr__(self):
        return '<User %r>' % self.username

""" Dummy user account """
class AnonUser:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<AnonUser %r>' % self.username

db.create_all()
check_config()
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
