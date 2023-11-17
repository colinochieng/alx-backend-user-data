#!/usr/bin/env python3
'''
Module for user Authentications
'''
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    '''
    desc: hashes user passcode using bcrypt
    param:
        password: user password
    return: hashed_user password
    '''
    salt = bcrypt.gensalt()
    password = password.encode('utf-8')

    return bcrypt.hashpw(password, salt)


def _generate_uuid() -> str:
    '''
    desc: a function to generate uuid
    return: string repr of uuid
    '''
    import uuid

    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, passwd: str) -> User:
        '''
        desc: function to register user, saves new
            user to the authentication database
        params:
            email: user mail
            passwd: user password
        '''
        # check if user already exist
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound as e:
            register_info = {
                    'email': email,
                    'hash_passwd': _hash_password(passwd)
                    }
            user = self._db.add_user(**register_info)

            return user

    def valid_login(self, email: str, password: str) -> bool:
        '''
        desc: method to check for user with the
            current email and validate password
        params:
            email: user  mail
            password: user password
        '''
        try:
            user = self._db.find_user_by(email=email)

            if user:
                if isinstance(user.hashed_password, str):
                    user_pwd = user.hashed_password.encode('utf-8')
                else:
                    user_pwd = user.hashed_password
                password = password.encode('utf-8')

                return bcrypt.checkpw(password, user_pwd)

        except NoResultFound as e:
            return False

    def create_session(self, email: str) -> str:
        '''
        desc: method to generate uuid and update user
            session id
        param:
            email: user mail
        return:  the session ID
        '''
        try:
            user = self._db.find_user_by(email=email)

            if user:
                session_id = {"session_id": _generate_uuid()}
                self._db.update_user(user.id, **session_id)

                return session_id['session_id']
        except NoResultFound as e:
            None

    def get_user_from_session_id(self, session_id: str) -> User:
        '''
        desc: retrives user from db based on session ID
        param:
            session_id: session id set as cookie
        return: User if session_id exists else None
        '''
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user if user else None

        except NoResultFound as e:
            None

    def destroy_session(self, user_id: int) -> None:
        '''
        desc: function to remove current user session
            from DB
        updates the corresponding user’s session ID to None
        '''
        try:
            user = self._db.update_user(user_id, session_id=None)
        except Exception as e:
            None

    def get_reset_password_token(self, email: str) -> str:
        '''
        desc: method to generate password reset token
        return: generated password token (str(UUID))
        '''
        try:
            user = self._db.find_user_by(email=email)

            if user:
                token = {'reset_token': _generate_uuid()}
                self._db.update_user(user.id, **token)

                return token['reset_token']

        except NoResultFound as e:
            raise ValueError

    def update_password(self, reset_token: str, pwd: str) -> None:
        '''
        desc: method to update user password
        params:
            reset_token: user password update verification token
            pwd: new user password
        '''
        try:
            user = self._db.find_user_by(reset_token=reset_token)

            # user exists
            hashed_password = {'hashed_password': _hash_password(pwd)}

            self._db.update_user(user.id, **hashed_password)
        except NoResultFound as e:
            raise ValueError
