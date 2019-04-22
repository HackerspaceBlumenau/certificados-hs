from argparse import ArgumentParser
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def parse_args():
    ap = ArgumentParser()

    ap.add_argument('--senha', type=str, required=True,
                    help='Senha utilizada para gerar a chave.')

    ap.add_argument('--caminho', type=str, required=True,
                    help='Caminho do arquivo para salvar a chave gerada.')

    return ap.parse_args()


if __name__ == '__main__':
    args = parse_args()

    password = args.senha.encode('utf-8')
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))

    with open(args.caminho, 'wb') as f:
        f.write(key)
