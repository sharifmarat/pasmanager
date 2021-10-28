#!/usr/bin/env python3

import pyotp
import bcrypt

# Deprecated
def tryToken(token, db):
    secretLastToken = db.getSecretAndLastToken("todo")

    if not secretLastToken:
        return False

    totp = pyotp.TOTP(secretLastToken[0])
    server_token = totp.now()
    last_valid_token = secretLastToken[1]

    if token != server_token or token == last_valid_token:
        return False

    db.updateLastToken("todo", server_token)

    return True


def login(username, password, token, db, add_if_not_exist=False):
    user = db.getUser(username)
    # TODO: remove soon
    #if not user and add_if_not_exist:
    #    hashpw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(12))
    #    if not db.addUser(username, token, hashpw.decode('utf8')):
    #        return False
    #    user = db.getUser(username)

    if not user:
        return False

    # 1. verify password
    if not bcrypt.checkpw(password.encode('utf8'), user['hash'].encode('utf8')):
        return False

    # 2. verify TOTP
    totp = pyotp.TOTP(user['token'])
    if not totp.verify(token):
        return False

    return True
