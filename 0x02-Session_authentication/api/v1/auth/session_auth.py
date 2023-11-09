#!/usr/bin/env python3
"""
SessionAuth class to manage the API authentication
"""

from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    '''Class SessionAuth'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''Creates a Session ID for a user_id'''
        if user_id is None or not isinstance(user_id, str):
            return None
        session = str(uuid4())
        self.user_id_by_session_id[session] = user_id
        return session
