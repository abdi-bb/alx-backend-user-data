#!/usr/bin/env python3
'''
Module auth
'''

from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    '''Returns a salted hash of the input password'''
    b_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(b_password, salt)


def _generate_uuid() -> str:
    '''Returns a str representation of a new UUID'''
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        '''Initialize Auth instance'''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''Returns the registered user'''
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(
                email=email, hashed_password=hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        '''Returns bool to indicate if valid login or not'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if user and bcrypt.checkpw(password.encode('utf-8'),
                                   user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        '''Returns Session ID'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_ID = _generate_uuid()
        if user:
            user.session_id = session_ID

        return session_ID
