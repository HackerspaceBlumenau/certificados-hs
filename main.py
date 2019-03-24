from argparse import ArgumentParser
from subprocess import run


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


def preencher_certificado(latex, nome, evento, data, duracao):
    latex = latex.replace('ALGUM NOME', nome.upper())
    latex = latex.replace('ALGUM EVENTO', evento.upper())
    latex = latex.replace('ALGUMA DATA', data)
    latex = latex.replace('ALGUMA DURACAO', duracao)
    return latex


if __name__ == '__main__':
    args = parse_args()

    nomes_emails = ler_nomes_emails(args.csv)
    template_latex = ler_tex(args.tex)

    for (nome, email) in nomes_emails:
        latex_certificado = preencher_certificado(template_latex, nome, args.evento,
                                                  args.data, args.duracao)

        with open('./latex_working_dir/temp.tex', 'w') as f:
            f.write(latex_certificado)

        run(
            ['pdflatex', 'temp.tex', '-output-directory=./latex_output/'],
            cwd='latex_working_dir'
        )
