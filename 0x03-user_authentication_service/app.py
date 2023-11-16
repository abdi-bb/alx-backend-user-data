#!/usr/bin/env python3
'''
Module app
'''

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = AUTH.register_user(email, password)

        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        new_session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', new_session_id)
        return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('welcome'))
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    '''Endpoint for /reset_password'''
    email = request.form.get('email')
    try:
        user = AUTH._db.find_user_by(email=email)
    except NoResultFound:
        abort(403)
    pwd_reset_token = AUTH.get_reset_password_token(email)
    return jsonify({"email": user.email, "reset_token": pwd_reset_token}), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ Endpoint that updates the user password """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except Exception as e:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
