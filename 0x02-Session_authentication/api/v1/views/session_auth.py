#!/usr/bin/env python3
""" Module of SessionAuth views
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def login_endpoint():
    '''Login endpoint'''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email is None or len(email) == 0:
            return jsonify({"error": "email missing"}), 400
        if password is None or len(password) == 0:
            return jsonify({"error": "password missing"}), 400

        try:
            users = User.search({'email': email})
        except Exception:
            return jsonify({"error": "no user found for this email"}), 404

        for user in users:
            if user.is_valid_password(password):
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                response = jsonify(user.to_json())
                session_name = os.getenv('SESSION_NAME')
                response.set_cookie(session_name, session_id)
                return response
        return jsonify({"error": "wrong password"}), 401
