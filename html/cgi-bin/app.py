#!/usr/bin/python3

import os

from flask import Flask
from flask import request
from flask import jsonify

class BadRequestResponse(Exception):
    status_code = 400

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        d = dict(())
        d['message'] = self.message
        return d

app = Flask(__name__)
app.debug = True

@app.errorhandler(BadRequestResponse)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/")
def index():
    return "Nothing to see here"

@app.route("/test")
def get_test():
    token = request.args.get('token')
    if not os.environ.get('KEY_DB'):
        raise BadRequestResponse("No database")
    if not token:
        raise BadRequestResponse("Bad token")

    db = os.environ.get('KEY_DB')

    from auth import tryToken
    from keymanager import KeyManager
    with KeyManager(db) as keys:
        if not tryToken(token, keys):
            raise BadRequestResponse("Bad token")
        return jsonify(keys.getList())

    return "Get test!"
