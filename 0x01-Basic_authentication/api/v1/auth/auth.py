#!/usr/bin/env python3
"""
Auth class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth():
    '''class Auth
    '''

    def require_auth(self, path: str, excluded_paths: List[str], strict_slashes=False) -> bool:
        '''Returns False now
        '''
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        if path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        '''Returns None
        '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''Returns None'''
        return None
