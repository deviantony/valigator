from bottle import post, run, request, abort
from filesystemmanager import FileSystemManager
from mailutils import MailUtils
from utils import generate_uuid, load_configuration
import importlib


@post('/validate/<backup>')
def validate(backup):
    """Use this endpoint to start a backup validation.
    You must specify the backup type in the endpoint.
    Specify JSON data for backup archive info.

    {
        'path': '/path/to/archive'
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

    workdir = ''.join([config['docker_temp_directory'], '/', generate_uuid()])

    try:
        filesystem.extract_archive(archive_path, workdir)
    except:
        notify_archive(archive_path)
        abort(400, 'An error occurred during archive extraction.')

    try:
        extension.run_container(workdir)
    except:
        notify_backup(archive_path)
        abort(400, 'An error occurred during archive restoration.')


def import_extension(extension_name):
    """This method will import a module from the 'extension' package.
    It will then instanciate an object from the module class.
    """
    module = importlib.import_module(
        ''.join(['extension.', extension_name]))
    extension_class = getattr(module, extension_name)
    return extension_class(config)


def notify_archive(archive_path):
    """Send a notification via email when the backup extraction fails."""
    mail.send_email('Automatic backup archive extraction failed',
                    'Unable to extract archive: ' + archive_path)


def notify_backup(archive_path):
    """Send a notification via email when the backup restoration fails."""
    mail.send_email('Automatic backup restoration failed',
                    'Unable to restore archive: ' + archive_path)

if __name__ == '__main__':
    config = load_configuration('valigator.yml')
    filesystem = FileSystemManager()
    mail = MailUtils(config['mail'])
    run(host=config['bind']['address'], port=config['bind']['port'])
