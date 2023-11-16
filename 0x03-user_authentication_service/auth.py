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

    def get_user_from_session_id(self, session_id: str) -> User:
        '''Returns User from session_id'''
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        '''Updates Session ID to None'''

        user = self._db.find_user_by(id=user_id)
        if user:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        '''Generates reset password token'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        pwd_reset_token = _generate_uuid()
        user.reset_token = pwd_reset_token
        return pwd_reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        '''Updates User password'''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_pwd = _hash_password(password)
        user.hashed_password = hashed_pwd
        user.reset_token = None
