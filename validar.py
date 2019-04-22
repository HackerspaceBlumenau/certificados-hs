from argparse import ArgumentParser
import json
import os
from pprint import PrettyPrinter

from PyPDF2 import PdfFileReader

import assinatura


def parse_args():
    ap = ArgumentParser()

    ap.add_argument('--pdf', type=str, required=True,
                    help='Caminho para o PDF do certificado a ser validado.')

    return ap.parse_args()


if __name__ == '__main__':
    args = parse_args()

    with open(args.pdf, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()

    dados = assinatura.verificar(info['/Subject'], os.environ['CERTIFICADO_CHAVE_ASSINATURA'])
    dados = json.loads(dados)

    print('===== ATENÇÃO =====')
    print('VALIDE OS DADOS ABAIXO COM OS DADOS NO PDF.')
    print('SE ALGUMA INFORMAÇÂO NÃO FOR IGUAL, O CERTIFICADO É INVÁLIDO...')
    pp = PrettyPrinter(indent=4)
    pp.pprint(dados)
