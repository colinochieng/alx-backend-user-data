#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
        desc: function to add User to the db
        params:
            email: user email
            hashed_passwd: User passcode
        Return: User object
        '''
        # create user
        user = User(email=email, hashed_password=hashed_password)

        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        '''
        desc: find user based on passed values
        param:
            kwargs: arbitrary keyword arguments
                decribing user
        Return: the first row found in the users table
            as filtered by the method’s input arguments
        '''
        if not kwargs:
            raise InvalidRequestError

        user_data = User.__table__.columns.keys()

        for key in kwargs.keys():
            if key not in user_data:
                raise InvalidRequestError

        # raises NoResultFound if no user found
        return self._session.query(User).filter_by(**kwargs).one()

    def update_user(self, user_id: int, **kwargs) -> None:
        '''
        desc: method to update user. Query the user using
            the id and uses the kwargs for updating
        params:
            user_id: user data to use for filtering
            kwargs: data to update
        raise: ValueError If an argument that does not
            correspond to a user attribute is passed
        '''
        user = self.find_user_by(id=user_id)

        for key in kwargs.keys():
            if not hasattr(User, key):
                raise ValueError

        for key, value in kwargs.items():
            if key != 'id':
                setattr(user, key, value)
        self._session.commit()
