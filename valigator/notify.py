import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# TODO: refactor
# TODO: handle notifier failures (Network unreachable...)


class MailNotifier(object):
    """Email notifier."""

    def __init__(self, configuration):
        self.server = configuration['smtp']['server']
        self.port = configuration['smtp']['port']
        self.timeout = configuration['smtp']['timeout']
        self.from_address = configuration['from_address']
        self.to_address = configuration['to_address']
        self.tls_auth = configuration['smtp']['tls_authentication']
        if self.tls_auth:
            self.user = configuration['smtp']['user']
            self.password = configuration['smtp']['password']

    def notify(self, subject, body):
        """ Initiate a SMTP session and send an email."""
        msg = MIMEMultipart()
        msg['From'] = self.from_address
        msg['To'] = self.to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        smtp = smtplib.SMTP(self.server, self.port,
                            timeout=self.timeout)
        if self.tls_auth:
            smtp.starttls()
            smtp.login(self.user, self.password)
        smtp.sendmail(self.from_address, self.to_address, msg.as_string())
        smtp.quit()

    def notify_archive(self, archive_path):
        """Send a notification via email
        when the backup extraction fails.
        """
        self.notify('Automatic backup archive extraction failed',
                    'Unable to extract archive: ' + archive_path)

    def notify_backup(self, archive_path):
        """Send a notification via email
        when the backup restoration fails.
        """
        self.notify('Automatic backup restoration failed',
                    'Unable to restore archive: ' + archive_path)

    def notify_docker(self, archive_path):
        """Send a notification via email
        when the docker container creation fails.
        """
        self.notify('Automatic backup restoration failed',
                    'Unable to create container for archive: ' + archive_path)
