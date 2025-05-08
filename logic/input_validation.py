"""
Author: R-Nixon
Creation Date: 2025-5-1
Last Modified: 2025-5-5
Description:
This module contains functions that validate user inputs.

Code References:
https://useful.codes/python-input-validation-and-sanitization/
https://blog.finxter.com/5-best-ways-to-implement-a-strong-password-checker-in-python/
"""

import re


def validate_email(email):
    """
    Function: validate_email
    Author: R-Nixon
    Date Created: 2025-5-1

    Purpose: Validate email user entries.  Matches the format of an email
    against a regex pattern.

    :param email: string, user's email
    :return: Boolean, True if pattern matches, False otherwise
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    # possible alternate pattern
    # pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(pattern, email):
        return True
    else:
        return False


def validate_password(password):
    """
    Function: validate_password
    Author: R-Nixon
    Date Created: 2025-5-1

    Purpose: Validate password user entries.  Matches the format of a password
    against regex parameters.

    :param password: string, user's password
    :return: Boolean, True if password is within parameters, False otherwise
    """
    # Password requirements: 6+ characters, uppercase, lowercase, number, special character
    length_regex = r'.{6,}'
    uppercase_regex = r'[A-Z]'
    lowercase_regex = r'[a-z]'
    digit_regex = r'[0-9]'
    special_char_regex = r'[^A-Za-z0-9]'

    if (re.search(length_regex, password) and
            re.search(uppercase_regex, password) and
            re.search(lowercase_regex, password) and
            re.search(digit_regex, password) and
            re.search(special_char_regex, password)):
        return True
    else:
        return False
