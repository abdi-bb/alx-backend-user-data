#!/usr/bin/env python3
'''
Module: 'encrypt_password'
'''

import bcrypt


def hash_password(password: str) -> str:
    '''Encrypts password'''
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())
