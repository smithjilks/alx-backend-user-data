#!/usr/bin/env python3
"""  class to manage the API authentication """
from flask import request
from typing import TypeVar, List


class Auth:
    """  class to manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ check if path need auth """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        len_path = len(path)
        if len_path == 0:
            return True

        slash_path = True if path[len_path - 1] == '/' else False

        temp_path = path
        if not slash_path:
            temp_path += '/'

        for elem in excluded_paths:
            len_elem = len(elem)
            if len_elem == 0:
                continue

            if elem[len_elem - 1] != '*':
                if temp_path == elem:
                    return False
            else:
                if elem[:-1] == path[:len_elem - 1]:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Method authorization header """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Validate user """
        return None
