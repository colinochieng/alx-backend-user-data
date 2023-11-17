#!/usr/bin/env python3

from app import app, AUTH

user = AUTH.register_user(
    'test@test.com',
    'test'
)

reset_token = AUTH.get_reset_password_token(
    'test@test.com'
)

AUTH.update_password(
    reset_token,
    'test'
)

if user.reset_token is not None:
    print("Reset token not set to none after updating\
            password. Password update did not work correctly.")
    exit(0)

print("OK", end='')
