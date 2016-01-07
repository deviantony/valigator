import smtplib
import traceback
import string
import cgi
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# TODO: handle notifier failures (Network unreachable...)


class MailNotifier(object):
    """Email notifier."""

    def __init__(self, configuration):
        self.server = configuration['smtp']['server']
        self.port = configuration['smtp']['port']
        self.timeout = configuration['smtp']['timeout']
        self.from_address = configuration['from_address']
        self.to_address = configuration['to_address']
        self.title = configuration['title']
        self.tls_auth = configuration['smtp']['tls_authentication']
        if self.tls_auth:
            self.user = configuration['smtp']['user']
            self.password = configuration['smtp']['password']

    def send_email(self, message):
        """Initiate a SMTP session and send an email."""
        msg = MIMEMultipart()
        msg['From'] = self.from_address
        msg['To'] = self.to_address
        msg['Subject'] = self.title
        msg.attach(MIMEText('<pre>' + cgi.escape(message) + '</pre>', 'html'))
        smtp = smtplib.SMTP(self.server, self.port,
                            timeout=self.timeout)
        if self.tls_auth:
            smtp.starttls()
            smtp.login(self.user, self.password)
        smtp.sendmail(self.from_address, self.to_address, msg.as_string())
        smtp.quit()

    def send_task_failure_report(self, task_report):
        """Sends a task failure report via e-mail."""
        message = task_failure_message(task_report)
        self.send_email(message)

    def send_report(self, report):
        """Sends a report via e-mail."""
        message = report_message(report)
        self.send_email(message)


def report_message(report):
    """Report message."""
    body = 'Error: return code != 0\n\n'
    body += 'Archive: {}\n\n'.format(report['archive'])
    body += 'Docker image: {}\n\n'.format(report['image'])
    body += 'Docker container: {}\n\n'.format(report['container_id'])
    body = '<pre>' + cgi.escape(body) + '</pre>'
    return body


def task_failure_message(task_report):
    """Task failure message."""
    trace_list = traceback.format_tb(task_report['traceback'])
    body = 'Error: task failure\n\n'
    body += 'Task ID: {}\n\n'.format(task_report['task_id'])
    body += 'Archive: {}\n\n'.format(task_report['archive'])
    body += 'Docker image: {}\n\n'.format(task_report['image'])
    body += 'Exception: {}\n\n'.format(task_report['exception'])
    body += 'Traceback:\n {} {}'.format(
        string.join(trace_list[:-1], ''), trace_list[-1])
    return body
