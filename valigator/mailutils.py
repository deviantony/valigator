import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailUtils(object):
    """Mailing utils.
    Use this object to send emails.
    It uses the mail parameters from the configuration file.
    """

    def __init__(self, mail_configuration):
        self.server = mail_configuration['smtp']['server']
        self.port = mail_configuration['smtp']['port']
        self.timeout = mail_configuration['smtp']['timeout']
        self.from_address = mail_configuration['from_address']
        self.to_address = mail_configuration['to_address']
        self.tls_auth = mail_configuration['smtp']['tls_authentication']
        if self.tls_auth:
            self.user = mail_configuration['smtp']['user']
            self.password = mail_configuration['smtp']['password']

    def send_email(self, subject, body):
        """ Initiate a SMTP session and send an email."""
        msg = MIMEMultipart()
        msg['From'] = self.from_address
        msg['To'] = self.to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP(self.server, self.port,
                          timeout=self.timeout) as smtp:
            if self.tls_auth:
                smtp.starttls()
                smtp.login(self.user, self.password)
            smtp.send_message(msg)
