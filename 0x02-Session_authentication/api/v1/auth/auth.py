#!/usr/bin/env python3
"""
Auth class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    '''class Auth
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Returns bool
        '''
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        path_has_slash = path.endswith('/')
        for excluded_path in excluded_paths:
            if not excluded_path.endswith('*'):
                if not excluded_path.endswith('/'):
                    excluded_path += '/'

                if path_has_slash and path == excluded_path:
                    return False

                if not path_has_slash and path + '/' == excluded_path:
                    return False
            else:
                # Remove the trailing wildcard character for comparison
                excluded_path = excluded_path[:-1]

                if path.startswith(excluded_path):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        '''Returns Authorization header
        '''
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        '''Returns None'''
        return None

    def session_cookie(self, request=None):
        '''Returns cookie value from the request'''
        if request is None:
            return None
        session_cookie_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_cookie_name)
