#!/usr/bin/env python3
"""
Auth class to manage the API authentication
"""
from flask import Auth
from typing import List


class Auth():
    '''class Auth
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Returns False now
        '''
        return False

    def authorization_header(self, request=None) -> str:
        '''Returns None
        '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''Returns None'''
        return None