#!/usr/bin/env python3
"""
Module fo string sessions
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from models.base import TIMESTAMP_FORMAT


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

        created_at = self.user_id_by_session_id[session_id].get("created_at")

        kwargs = {
            "session_id": session_id,
            "user_id": user_id,
        }

        user_session = UserSession(**kwargs)

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

        if self.session_duration > 0:
            created_at = user_session.created_at

            if created_at is None:
                # destroy the session
                user_session.remove()
                return None

            expiration_time = created_at + timedelta(
                seconds=self.session_duration)

            if datetime.utcnow() > expiration_time:
                # destroy the session
                user_session.remove()
                return None

        return user_session.user_id

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
