#!/usr/bin/env python3
"""
SessionAuth class to manage the API authentication
"""

from api.v1.auth.auth import Auth
from uuid import uuid4
import os
from models.user import User


class SessionAuth(Auth):
    '''Class SessionAuth'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''Creates a Session ID for a user_id'''
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''Returns user_id based on the session_id'''
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''Identify a user using Session ID'''
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        '''Deletes the user session/logout'''
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
