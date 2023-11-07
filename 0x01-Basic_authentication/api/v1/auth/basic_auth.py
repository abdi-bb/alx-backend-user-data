#!/usr/bin/env python3
"""
BasicAuth class to manage the API authentication
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''Class BasicAuth to manage API authentication
    '''

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        '''Returns Base64 part of Authorization'''
        if authorization_header is None:
            return None
        elif not isinstance(authorization_header, str):
            return None
        elif not authorization_header.startswith('Basic'):
            return None
        else:
            return authorization_header[5:]
