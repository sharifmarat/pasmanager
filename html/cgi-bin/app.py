#!/usr/bin/python3

import os

from flask import Flask
from flask import request
from flask import jsonify
from flask import session

from dotenv import load_dotenv
load_dotenv()

import auth
from keymanager import KeyManager

def get_secret_key():
    key = os.environ.get('SECRET')
    if not key:
        raise Exception("No secret defined")
    return key.encode('utf8')

app = Flask(__name__)
app.secret_key = get_secret_key()
app.debug = True

class BadRequestResponse(Exception):
    status_code = 400

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        d = dict(())
        d['message'] = self.message
        return d

@app.before_request
def check_env():
    if not os.environ.get('KEY_DB'):
        raise BadRequestResponse("No database")

def require_auth():
    if not 'user' in session:
        raise BadRequestResponse("No auth")

@app.errorhandler(BadRequestResponse)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/")
def index():
    require_auth()
    return "Logged in as " + session['user']

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    token = request.form.get('token')
    if not username or not password or not token:
        raise BadRequestResponse("Auth Error")

    db_path = os.environ.get('KEY_DB')
    with KeyManager(db_path) as db:
        if auth.login(username, password, token, db):
            session['user'] = username
            return jsonify({'status': 0})
    raise BadRequestResponse("Auth Error")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return "Success"

@app.route("/getkey", methods=['POST'])
def get_key():
    require_auth()
    id = request.form.get('id')
    db_path = os.environ.get('KEY_DB')
    with KeyManager(db_path) as db:
        cipher = db.getCipher(id)
        if not cipher:
            raise BadRequestResponse("Cannot get key")
        return jsonify({'cipher': cipher})

@app.route("/addkey", methods=['POST'])
def add_key():
    require_auth()
    id = request.form.get('id')
    cipher = request.form.get('cipher')

    db_path = os.environ.get('KEY_DB')
    with KeyManager(db_path) as db:
        if not db.addCipher(id, cipher):
            raise BadRequestResponse("Cannot add key")
        return "Success"

@app.route("/getlist")
def get_test():
    require_auth()
    db_path = os.environ.get('KEY_DB')
    with KeyManager(db_path) as db:
        return jsonify(db.getList())
