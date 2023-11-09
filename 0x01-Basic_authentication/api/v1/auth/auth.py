#!/usr/bin/env python3
'''
Module for Auth class
'''
from flask import request
from typing import List, TypeVar


class Auth:
    '''
    class to manage the API authentication
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
        desc:method to check if a route requires authentication
        params:
            path: route to check
            excluded_paths: routes that don't need authentication
        returns:
            -> False: if path is in excluded_paths
            -> True: if the path is not in the list of strings
                excluded_paths or if path is None
                or  if excluded_paths is None or empty

        More_info: the method must be slash tolerant:
            path=/api/v1/status and path=/api/v1/status/
            must be returned False if excluded_paths contains
            /api/v1/status/
        '''
        if path is None or excluded_paths is None:
            return True

        # targeting slash tolerance
        if (
            path[0:-1] in excluded_paths
            or (path + '/') in excluded_paths
        ):
            return False

        if len(excluded_paths) == 0 or path not in excluded_paths:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        '''
        desc: method for app-request validation
        params:
            request: the Flask request object
        '''
        if request is None:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        desc:
        params:
            request: the Flask request object
        '''
        return None
