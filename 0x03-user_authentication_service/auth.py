#!/usr/bin/env python3
'''
Module auth
'''

import bcrypt


def _hash_password(password: str) -> bytes:
    '''Returns a salted hash of the input password'''
    b_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(b_password, salt)
