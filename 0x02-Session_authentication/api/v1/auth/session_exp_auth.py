#!/usr/bin/env python3
"""
SessionExpAuth class to manage the API authentication
"""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    '''Class SessionExpAuth'''

    def __init__(self) -> None:
        '''Instantiation'''
        try:
            session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        '''
        Overloading create_session method of SessionAuth
        Create Session ID for user_id
        '''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''
        Overload user_id_for_session_id of SessionAuth
        Returns User ID based on Session ID
        '''
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        if 'created_at' not in session_dict.keys():
            return None

        created_at = session_dict.get('created_at')
        now = datetime.now()
        allowed_window = created_at + timedelta(seconds=self.session_duration)
        if allowed_window < now:
            return None

        return session_dict.get('user_id')
