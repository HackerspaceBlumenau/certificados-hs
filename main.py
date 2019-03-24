from argparse import ArgumentParser
from subprocess import run
from os import mkdir, path
from shutil import rmtree, move
import os


LATEX_WORKING_DIR = './latex_working_dir'


def parse_args():
    ap = ArgumentParser()

    ap.add_argument('--csv', type=str, required=True,
                    help='Caminho para o arquivo csv com nome,email.')

    ap.add_argument('--evento', type=str, required=True,
                    help='Nome do evento.')

    ap.add_argument('--data', type=str, required=True,
                    help='Data do evento.')

    ap.add_argument('--duracao', type=str, required=True,
                    help='Duração do evento.')

    ap.add_argument('--tex', type=str, required=True,
                    help='Caminho para o arquivo LATEX de template.')

    return ap.parse_args()


def ler_nomes_emails(caminho_csv):
    with open(caminho_csv, 'r') as f:
        nomes_emails = f.readlines()
    
    nomes_emails = (s.split(',') for s in nomes_emails)
    return [(n.strip(), e.strip()) for (n, e) in nomes_emails]


def ler_tex(caminho_tex):
    with open(caminho_tex, 'r') as f:
        return f.read()


def gerar_certificado(latex_certificado, id, latex_working_dir, output_dir):
    temp_dir = f'{latex_working_dir}/{id}'
    if path.exists(temp_dir):
        rmtree(temp_dir)

    mkdir(temp_dir)

    arquivo = 'certificado.tex'
    arquivo_certificado = f'{latex_working_dir}/{id}/{arquivo}'
    with open(arquivo_certificado, 'w') as f:
        f.write(latex_certificado)

    latex_arquivo_certificado = f'{id}/{arquivo}'
    with open(os.devnull, 'w') as devnull:
        run(
            ['pdflatex', f'-output-directory={id}', latex_arquivo_certificado],
            cwd=latex_working_dir,
            stdout=devnull
        )

    pdf = arquivo.replace("tex", "pdf")
    temp_pdf = f'{latex_working_dir}/{id}/{pdf}'
    final_pdf = f'{output_dir}/certificado_{id}.pdf'
    move(temp_pdf, final_pdf)

    rmtree(temp_dir)

    return final_pdf


def preencher_certificado(latex, nome, evento, data, duracao):
    latex = latex.replace('ALGUM NOME', nome.upper())
    latex = latex.replace('ALGUM EVENTO', evento.upper())
    latex = latex.replace('ALGUMA DATA', data)
    latex = latex.replace('ALGUMA DURACAO', duracao)
    return latex


if __name__ == '__main__':
    args = parse_args()

    certificados_dir = './temp_certificados'
    if path.exists(certificados_dir):
        rmtree(certificados_dir)
    
    mkdir(certificados_dir)

    nomes_emails = ler_nomes_emails(args.csv)
    template_latex = ler_tex(args.tex)

    for (i, (nome, email)) in enumerate(nomes_emails):
        latex_certificado = preencher_certificado(template_latex, nome, args.evento,
                                                  args.data, args.duracao)

        caminho_certificado_pdf = gerar_certificado(
            latex_certificado,
            id=i,
            latex_working_dir=LATEX_WORKING_DIR,
            output_dir=certificados_dir
        )



    # rmtree(certificados_dir)