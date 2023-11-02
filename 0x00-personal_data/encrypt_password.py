#!/usr/bin/env python3
'''
Module: 'encrypt_password'
'''

import bcrypt


def hash_password(password: str) -> str:
    '''Encrypts password'''
    password = b'{password}'
    return bcrypt.hashpw(password, bcrypt.gensalt())
