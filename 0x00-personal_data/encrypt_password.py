#!/usr/bin/env python3
'''
Module: 'encrypt_password'
'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''Encrypts password'''
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''Checks if hashed_password and password are valid to eache other'''
    return bcrypt.checkpw(password.encode(), hashed_password)
