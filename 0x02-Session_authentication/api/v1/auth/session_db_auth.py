#!/usr/bin/env python3
"""
Module fo string sessions
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Scheme for storing Session Data
    """

    def create_session(self, user_id=None) -> str:
        """
        creates and stores new instance of UserSessio
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        user_session = UserSession(session_id=session_id, user_id=user_id)

        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        returns the User ID by requesting UserSession
        in the database based on session_id
        """
        if not session_id:
            return None

        UserSession.load_from_file()

        try:
            objs = UserSession.search({"session_id": session_id})
        except KeyError as e:
            return None

        if not objs:
            return None

        user_session = objs[0]

        return user_session.to_json().get("user_id")

    def destroy_session(self, request=None) -> bool:
        """
        destroys the UserSession based on the
            Session ID from the request cookie
        """
        session_id = self.session_cookie(request)

        if not session_id:
            return False

        UserSession.load_from_file()

        try:
            objs = UserSession.search({"session_id": session_id})
        except KeyError as e:
            return None

        if not objs:
            return False

        user_session = objs[0]

        # delete session object from storage
        user_session.remove()
        return True
