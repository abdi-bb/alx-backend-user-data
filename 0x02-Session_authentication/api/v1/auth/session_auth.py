#!/usr/bin/env python3
"""
SessionAuth class to manage the API authentication
"""

from api.v1.auth.auth import Auth
from uuid import uuid4
import os


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

    def session_cookie(self, request=None):
        '''Returns cookie value from the request'''
        if request is None:
            return None
        session_cookie_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_cookie_name)