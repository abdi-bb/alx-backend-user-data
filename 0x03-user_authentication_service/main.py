#!/usr/bin/env python3
'''
Main module for tsting purpose
'''

import requests

BASE_URL = "http://localhost:5000"  # Update with your actual server URL
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    ''' Register user'''
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    '''Using wrong password for logging in'''
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    '''Login'''
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    '''Unlogged profile'''
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    '''Logged profile'''
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    '''Logout'''
    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 302  # Assuming you're using redirect for logout


def reset_password_token(email: str) -> str:
    '''Password_token reseting'''
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''Update password'''
    url = f"{BASE_URL}/reset_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, data=data)
    assert response.status_code == 200


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
