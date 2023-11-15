#!/usr/bin/env python3
'''
- Module for testing Authentication
    of the Flask app in module app
- Create one function for each of the tasks (functions)
- Use the requests module to query the
    web server for the corresponding end-point
- Use assert to validate the response’s
    expected status code and payload (if any)
'''
import requests


URL = 'http://localhost:5000/'


def register_user(email: str, password: str) -> None:
    '''
    desc: a function to mock user registration
    params:
        email: user email
        password: user password
    '''
    data = {'email': email, 'password': password}
    response = requests.post(f'{URL}users', data=data)

    assert response.status_code == 200
    msg = {"email": email, "message": "user created"}
    assert response.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    '''
    desc: mocks request for user login
        uses wrong password to test failure response
    params:
        email: user email
        password: invalid user passcode
    '''
    data = {'email': email, 'password': password}
    response = requests.post(f'{URL}sessions', data=data)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    '''
    desc: mocks login with loging with corret password
    params:
        email: user email
        password: valid user passcode
    return: User session ID after successful login
    '''
    data = {'email': email, 'password': password}
    response = requests.post(f'{URL}sessions', data=data)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    assert 'session_id' in response.cookies.keys()

    return response.cookies.get('session_id') 


def profile_unlogged() -> None:
    '''
    desc: mocks login without valid session id
    '''
    cookies = {'session_id': 'Invalid session id'}
    response = requests.post(f'{URL}profile', cookies=cookies)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    '''
    desc: mocks profile access using valid session id
    params:
        session_id: session id to be used as cookie
    '''
    cookies = {'session_id': session_id}
    response = requests.post(f'{URL}profile', cookies=cookies)

    assert response.status_code == 200
    assert response.json() == {'email': "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    '''
    desc: mocks user log out
    params:
        session_id: valid session ID
    '''
    cookies = {'session_id': session_id}
    response = requests.delete(f'{URL}sessions', cookies=cookies)

    assert response.status_code == 200
    assert response.url == 'http://localhost:5000/'

    assert response.json() == {'message': 'Bienvenue'}


def reset_password_token(email: str) -> str:
    '''
    desc: mocks request for resetting user password
    params:
        email: user email
    return: reset password token
    '''
    


def update_password(email: str, reset_token: str, new_password: str) -> None:
    pass

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


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

