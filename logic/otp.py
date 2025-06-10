"""
Author: R-Nixon
Creation Date: 2025-5-23
Last Modified: 2025-6-10
Description:
This module contains functions for generating and verifying a
time-based one-time-password code.
The otp code is used in signup.py to implement email confirmation at
user sign up.

Code Reference:
https://github.com/walid11111/Multi-Factor-Auth-System
https://stackoverflow.com/questions/51133948/change-default-expiry-period-of-pyotp
"""

import pyotp
import time

# Amount of time the user has to enter the correct otp code
INTERVAL = 180


def generate_otp_code():
    """
        Function: generate_otp_code
        Author: R-Nixon
        Date Created: 2025-5-27

        Purpose: Generate a totp object and an otp code.
        The generated totp code is good for 5 minutes.

        :return: tuple (totp, otp_code)
        """
    secret_key = pyotp.random_base32()
    totp = pyotp.TOTP(secret_key, interval=INTERVAL)
    # Determine the current time within the interval.
    now = time.time()
    # Determine how much time remains until the next interval.
    remainder = INTERVAL - (now % INTERVAL)
    # Wait until the start of the next interval.
    time.sleep(remainder)
    # Grab the otp token at the start of the interval.
    otp_code = totp.now()
    return totp, otp_code


def verify_otp_code(totp, code_entry):
    """
        Function: verify_otp_code
        Author: R-Nixon
        Date Created: 2025-5-27

        Purpose: Verify an otp code entry using a totp object.

        :param totp: TOTP object
        :param code_entry: string, otp code entry to be verified
        :return: boolean True False
        """
    return totp.verify(code_entry)
