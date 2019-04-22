import base64

from cryptography.fernet import Fernet


def gerar(conteudo, caminho_chave):
    with open(caminho_chave, "rb") as key_file:
        fernet = Fernet(key_file.read())

    assinatura = fernet.encrypt(conteudo.encode('utf-8'))
    return base64.urlsafe_b64encode(assinatura).decode('utf-8')


def verificar(conteudo, caminho_chave):
    with open(caminho_chave, "rb") as key_file:
        fernet = Fernet(key_file.read())
    
    conteudo = base64.urlsafe_b64decode(conteudo)
    return fernet.decrypt(conteudo).decode('utf-8')
