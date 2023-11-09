#!/usr/bin/env pyton3
"""
Session Authentication Object
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """
    Flask - Session Authentication
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        desc: creates a Session ID or a user_id
        param:
            user_id: Authenticated user's Id
        return: Session ID
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        else:
            session_id = str(uuid.uuid4())
            self.__class__.user_id_by_session_id.update({session_id: user_id})

            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        desc: method to retrive user_id based on session id
        param:
            session_id: Session Id used as key in user_id_by_session_id
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar("User"):
        """
        desc: method that returns a User instance based on a cookie value
            - uses the cookie value to retrive user ID from
                from session dictionary and then use the ID to retrive
                the respective user from the database
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        '''
        desc: method to delete the user session / logout
        '''
        if (
            not request or not self.session_cookie(request)
            or not self.user_id_for_session_id(self.session_cookie(request))
        ):
            return False
        else:
            self.__class__.user_id_by_session_id.pop(
                self.session_cookie(request)
            )
            return True
