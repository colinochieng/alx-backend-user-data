#!/usr/bin/env python3
"""
Basic auth's Module
Uses base64 algorithms for basic authentications
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from models.base import DATA


class BasicAuth(Auth):
    """
    class for Basic Authentication
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        desc: method to return the Base64 part of the Authorization
            header for a Basic Authentication
        param:
            authorization_header: encoded header
        assumes authorization_header contains only one Basic
        """
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None
        else:
            return authorization_header.replace("Basic ", "")

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        desc: method that returns the decoded value of a Base64 string
        param:
            base64_authorization_header: string to decode
        """
        if (
            base64_authorization_header is None
            or not isinstance(base64_authorization_header, str)
        ):
            return None

        try:
            return base64.b64decode(
                base64_authorization_header).decode("utf-8")
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        desc: method to return the user email and
            password from the Base64 decoded value
        param:
            decoded_base64_authorization_header: string to extract from
        assume decoded_base64_authorization_header will contain only one :
        """
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or ":" not in decoded_base64_authorization_header
        ):
            return None, None

        return tuple(decoded_base64_authorization_header.split(":", 1))

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> object:
        """
        desc: method that returns the User instance based
            on his email and password
        """
        if (
            user_email is None
            or not isinstance(user_email, str)
            or user_pwd is None
            or not isinstance(user_pwd, str)
        ):
            return None

        # extract all user in db
        User.load_from_file()

        # if no user in DB
        if len(DATA[User.__name__]) == 0:
            return None
        objs = User.search(
            {
                "email": user_email,
            }
        )

        if not objs:
            return None

        user = objs[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> object:
        """
        retrives user based on flask-request authentification info
        """
        auth = self.authorization_header(request)
        if auth is None:
            return None

        auth_str = self.extract_base64_authorization_header(str(auth))
        if auth_str is None:
            return None

        decoded_auth = self.decode_base64_authorization_header(auth_str)
        if decoded_auth is None:
            return None

        user_credentials = self.extract_user_credentials(decoded_auth)
        if None in user_credentials:
            return None

        return self.user_object_from_credentials(*user_credentials)
