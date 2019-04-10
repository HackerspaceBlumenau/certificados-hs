import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


def obter_chave_privada(caminho_chave_privada, senha):
    with open(caminho_chave_privada, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=senha.encode('utf8'),
            backend=default_backend()
        )


def gerar(conteudo, caminho_chave_privada, senha_chave_privada):
    chave = obter_chave_privada(caminho_chave_privada, senha_chave_privada)
    assinatura = chave.sign(
        conteudo.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return base64.urlsafe_b64encode(assinatura).decode('utf-8')
