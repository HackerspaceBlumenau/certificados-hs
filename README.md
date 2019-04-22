# certificados-hs

Repositório com o emissor e validador de certificados do Hackerspace Blumenau.

Para gerar um certificado você precisa de um email no GMail (suportado no momento) e o _pdflatex_.

Existe um template incluso nesse repositório, mas você pode criar o seu (mais detalhes abaixo).

# Instalando

`git clone <este repositório>`

**Para evitar conflitos com pacotes do sistema, inicie um ambiente virtual.**

`pip install -r requirements.txt`

**Gere uma chave (guarde-a) que será usada para assinar e recuperar os dados dos certificados.**

`python gerar_chave.py --senha <uma senha> --caminho ./certificados.key`

_Guarde essa chave!_ :)

# Emitindo certificados

Antes de emitir um certificado você precisa exportar três variáveis de ambiente para configuração.

```
export CERTIFICADO_CHAVE_ASSINATURA=certificados.key # caminho da chave gerada acima
export CERTIFICADO_EMAIL=meuemail@gmail.com # Email usado para autenticação SMTP e envio
export CERTIFICADO_EMAIL_SENHA="uma senha" # senha do email
```

Note que a autenticação pode falhar porque o GMail pode bloquear essas conexões.
Para mais informações, acesse [essa página do Google](https://support.google.com/a/answer/6260879?hl=en).

Agora, podemos emitir os certificados.

`python emitir.py --evento "Nome do meu evento" --data "01/01/2019" --duracao "3 horas" --csv nomes_emails.csv --tex template.tex`

# Validando certificados

Esse processo ainda está manual. Baixe o PDF do certificado em um diretório qualquer e execute

`python validar.py --pdf caminho/para/pdf/certificado.pdf`

_Note que a a variável de ambiente `CERTIFICADO_CHAVE_ASSINATURA` deve estar com a chave usada para assinar o certificado._

Agora, você precisa comparar as informações do _terminal_ com os dados no certificado.

# Alterando o template

Por padrão, esse repositório disponibiliza um `template.tex`, mas você pode usar o seu.

Você pode usar qualquer template que compile no seu LaTeX local, apenas deve deixar os seguintes _placeholders_ no seu arquivo `.tex` para que sejam substituídos durante a compilação/emissão.

_Placeholders_:

* `NOME-PARTICIPANTE`: será substituído pelo nome do participante
* `NOME-EVENTO`: será substituído pelo nome do evento
* `DATA-EVENTO`: será substituído pela data do evento
* `DURACAO-EVENTO`: será substituído pela duração do evento
* `DATA-EMISSAO`: será substituído pela data de emissão do certificado
* `HASH-VALIDACAO`: será substituído pelo hash de assinatura do certificado
