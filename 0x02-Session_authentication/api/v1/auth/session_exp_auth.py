#!/usr/bin/env python3
"""
Session expiration Module
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Session Object with expiration period
    """

    def __init__(self) -> None:
        """Overloading"""
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except (ValueError, TypeError) as e:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """
        Overloads
        creates time-based sessions
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.__class__.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }

        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Overloads the base method
        desc: method to retrive user_id based on session id
        param:
            session_id: Session Id used as key in user_id_by_session_id
        """
        if (
            not session_id
            or session_id not in self.__class__.user_id_by_session_id.keys()
        ):
            return None

        session_dict = self.__class__.user_id_by_session_id[session_id]

        if self.session_duration > 0:
            created_at = session_dict.get("created_at")
            if created_at is None:
                return None

            expiration_time = created_at + timedelta(
                    seconds=self.session_duration)
            if datetime.now() > expiration_time:
                return None

        return session_dict.get("user_id")
