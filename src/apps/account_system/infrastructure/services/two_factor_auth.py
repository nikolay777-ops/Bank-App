import qrcode
import pyotp
from random import SystemRandom
import base64

def generate_secret_key():
    random_bytes = SystemRandom().getrandbits(256).to_bytes(32, byteorder='big')
    return base64.b32encode(random_bytes).decode('utf-8')


# otp - это тот код(шестизначный), который вы вводите из приложения гугл аунтификатора
def verify_otp(secret, otp) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)


def generate_qr_code(username, secret):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=username, issuer_name="YourApp")

    img = qrcode.make(uri)

    return img