#!/usr/bin/env python3

import pyotp

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
