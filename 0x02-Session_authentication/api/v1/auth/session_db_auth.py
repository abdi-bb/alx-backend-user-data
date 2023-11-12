#!/usr/bin/env python3
"""
SessionDBAuth class to manage the API authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    '''Class SessionDBAuth'''

    def create_session(self, user_id=None):
        '''
        Create and store a new instance of SessionDBAuth and
        return the Session ID.
        '''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        kwargs = {
            'user_id': user_id,
            'session_id': session_id
        }
        user_sessions = UserSession(**kwargs)
        user_sessions.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''
        Return the User ID
        by querying SessionDBAuth in the database based on session_id.
        '''
        user_id = UserSession.search({'session_id': session_id})
        if not user_id:
            return None
        return user_id

    def destroy_session(self, request=None):
        '''
        Destroy the SessionDBAuth
        based on the Session ID from the request cookie.'''
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False
        user_sessions[0].remove()
        return True
