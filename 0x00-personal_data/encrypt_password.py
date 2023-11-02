#!/usr/bin/env python3
'''
Module for Encrypting passwords:
    password hashing using bcrypt
'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''
    desc: function that hashes passcode
    params:
        password: user passcode
    return: bcrypt enciphered passcode
        a salted, hashed password, which is a byte string
    '''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''
    desc: function to validate user passcode
    params:
        hashed_password: user strored encrypted passcode
        password: passcode to validate
    return: True or False
    '''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
