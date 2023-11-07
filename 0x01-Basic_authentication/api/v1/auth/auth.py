#!/usr/bin/env python3
"""
Auth class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


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
            if not excluded_path.endswith('/'):
                excluded_path += '/'

            if path_has_slash and path == excluded_path:
                return False

            if not path_has_slash and path + '/' == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        '''Returns None
        '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''Returns None'''
        return None
