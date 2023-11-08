#!/usr/bin/env python3
"""
BasicAuth class to manage the API authentication
"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    '''Class BasicAuth to manage API authentication
    '''

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''Returns Base64 part of Authorization'''
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic'):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        '''Returns Decoded value of Base64 string
        base64_authorization_header
        '''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_byte = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_byte.decode('utf-8')
            return decoded_str
        except Exception as e:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        '''Returns user email and password from Base64 decoded value
        '''
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(':')
        return (email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''Returns user obj'''
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''Returns User instance for a request
        '''
        auth_header = self.authorization_header(request)
        if auth_header:
            encoded = self.extract_base64_authorization_header(auth_header)
            if encoded:
                decoded = self.decode_base64_authorization_header(encoded)
                if decoded:
                    email, pwd = self.extract_user_credentials(decoded)
                    if email and pwd:
                        user = self.user_object_from_credentials(email, pwd)
                        return user

        return None
