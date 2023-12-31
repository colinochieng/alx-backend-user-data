#!/usr/bin/env python3
'''
Module for storing user sessions
'''
from models.base import Base


class UserSession(Base):
    '''
    Scheme for storing user session data
    '''
    def __init__(self, *args: list, **kwargs: dict) -> None:
        '''
        Intilaize Objects
        '''
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
