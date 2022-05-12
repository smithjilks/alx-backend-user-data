#!/usr/bin/env python3
"""
This script implements a hash_password function
that expects one string argument name password
and returns a salted, hashed password, which is a byte string.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ expects one string argument name
    password and returns a salted, hashed password, which is a byte string """
    encoded_pwd = password.encode()

    return bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ expects 2 arguments and returns a boolean """
    encoded_pwd = password.encode()
    if bcrypt.checkpw(encoded_pwd, hashed_password):
        return True
    return False
