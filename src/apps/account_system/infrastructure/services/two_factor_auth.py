import qrcode
import pyotp
from random import SystemRandom
import base64


def generate_secret_key():
    return pyotp.random_base32()


# otp - это тот код(шестизначный), который вы вводите из приложения гугл аунтификатора
def verify_otp(secret, otp) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)


def generate_qr_code(username, secret):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=username, issuer_name="Bank-app")

    img = qrcode.make(uri)

    return img