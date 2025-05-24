import pyotp


def generate_code():
    secret_key = pyotp.random_base32()
    hotp = pyotp.HOTP(secret_key)
    otp_code = hotp.at(0)
    print(otp_code)
    return otp_code


def send_confirmation_email():
    pass
