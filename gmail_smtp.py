import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class GmailSmtp:

    def autenticar(self, usuario, senha):
        self._server = smtplib.SMTP('smtp.gmail.com', 587)
        self._server.starttls()
        self._server.login(usuario, senha)

    def fechar(self):
        self._server.quit()

    def enviar_certificado_por_email(self, dados_email):
        msg = MIMEMultipart()

        msg['From'] = dados_email['de']
        msg['To'] = dados_email['para']
        msg['Subject'] = dados_email['assunto']

        msg.attach(MIMEText(dados_email['conteudo'], 'plain'))

        attachment = open(dados_email['caminho_certificado_pdf'], "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename=certificado.pdf")
        msg.attach(part)

        self._server.sendmail(dados_email['de'], dados_email['para'], msg.as_string())
