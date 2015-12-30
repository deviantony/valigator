import click
from os import path
from bottle import post, run, request, abort
from tarfile import TarError
from mailutils import MailUtils
from utils import generate_uuid, load_configuration, extract_archive
from dockermanager import DockerManager

config = {}
mail = {}
docker = {}


@post('/validate/<backup>')
def validate(backup):
    """Use this endpoint to start a backup validation.
    You must specify the backup type in the endpoint.
    Specify JSON data for backup archive info.

    {
        'archive_path': '/path/to/archive'
    }

    First, it will try to search for an existing extension definition
    in the configuration file.

    It will then extract the backup archive into a unique folder
    in the temporary directory specified in the configuration.
    A notification is sent if this step fails.

    Once extracted, a Docker container will be started and will
    start a restoration procedure.
    A notification is sent if this step fails.
    """
    data = request.json
    if not data:
        abort(400, 'No data received')
    archive_path = data['archive_path']

    try:
        config['extension'][backup]
    except KeyError:
        abort(400, 'No extension configuration found for: ' + backup)

    workdir = ''.join([config['valigator']['tmp_dir'], '/', generate_uuid()])
    backup_data = {'archive_path': archive_path,
                   'workdir': workdir,
                   'image': config['extension'][backup]['image'],
                   'command': config['extension'][backup]['command']}

    try:
        extract_archive(archive_path, workdir)
    except (OSError, TarError):
        notify_archive(archive_path)
        abort(400, 'An error occurred during archive extraction.')

    exit_code = docker.run_container(backup_data)
    if exit_code != 0:
        notify_backup(archive_path)
        abort(400, 'An error occurred during backup restoration.')


def notify_archive(archive_path):
    """Send a notification via email when the backup extraction fails."""
    mail.send_email('Automatic backup archive extraction failed',
                    'Unable to extract archive: ' + archive_path)


def notify_backup(archive_path):
    """Send a notification via email when the backup restoration fails."""
    mail.send_email('Automatic backup restoration failed',
                    'Unable to restore archive: ' + archive_path)


@click.command()
@click.option('--conf', default='/etc/valigator/valigator.yml',
              help='Valigator configuration file',
              show_default=True)
def main(conf):
    """Main function, entry point of the program."""
    global config, mail, docker
    config = load_configuration(conf)
    mail = MailUtils(config['mail'])
    docker = DockerManager(config)
    run(host=config['valigator']['host'], port=config['valigator']['port'])
