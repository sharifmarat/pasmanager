#!/usr/bin/env python3

import json
import os
import sys
import cgi
import cgitb
cgitb.enable(display=0)

if not os.environ.get('KEY_DB'):
    print("Content-Type: text/plain\n")
    print(json.dumps({'status': 1, 'message': 'Cannot find database. Set environment variable'}))
    sys.exit()

form = cgi.FieldStorage()
if "id" not in form or "cipher" not in form or "token" not in form:
    print("Content-Type: text/plain\n")
    print(json.dumps({'status': 1, 'message': 'Request is not correct'}))
    sys.exit()

db = os.environ.get('KEY_DB')
id = form.getfirst("id")
cipher = form.getfirst("cipher")
token = form.getfirst("token")

from auth import tryToken
from keymanager import KeyManager
with KeyManager(db) as keys:
    if not tryToken(token, keys):
        print("Content-Type: text/plain\n")
        print(json.dumps({'status': 1, 'message': 'Auth failed'}))
        sys.exit()

    if keys.addCipher(id, cipher):
        print("Content-Type: text/plain\n")
        print(json.dumps({'status': 0, 'message': 'Add done'}))
    else:
        print("Content-Type: text/plain\n")
        print(json.dumps({'status': 1, 'message': 'Could not update database'}))

