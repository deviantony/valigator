from bottle import post, run, request, abort
from filesystemmanager import FileSystemManager
from mailutils import MailUtils
from utils import get_uuid
from yaml import safe_load
import importlib


@post('/validate/<backup>')
def validate(backup):
    """Use this endpoint to start a backup validation.
    You must specify the backup type in the endpoint.
    Specify JSON data for backup archive info.

    {
        "path": "/path/to/archive"
    }

    First, it will try to search for an existing extension module
    in the extension package.

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
    archive_path = data['path']

    try:
        extension = import_extension(backup)
    except:
        abort(400, 'No extension found for: ' + backup)

    workdir = ''.join([config["docker_temp_directory"], '/', get_uuid()])

    try:
        manager.extract_archive(archive_path, workdir)
    except:
        notify_archive(archive_path)
        abort(400, 'An error occured during archive extraction.')

    try:
        extension.run_container(workdir)
    except:
        notify_backup(archive_path)
        abort(400, 'An error occured during archive restoration.')


def import_extension(extension_name):
    module = importlib.import_module(
        ''.join(['extension.', extension_name]))
    extension_class = getattr(module, extension_name)
    return extension_class(config)


def notify_archive(archive_path):
    mail.send_email('Automatic backup archive extraction failed',
                    'Unable to extract archive: ' + archive_path)


def notify_backup(archive_path):
    mail.send_email('Automatic backup restoration failed',
                    'Unable to restore archive: ' + archive_path)


def load_configuration(configuration_file):
    with open(configuration_file, 'r') as stream:
        config = safe_load(stream)
        return config

if __name__ == '__main__':
    config = load_configuration("config.yml")
    manager = FileSystemManager()
    mail = MailUtils(config["mail"])
    run(host=config['bind']['address'], port=config['bind']['port'])
