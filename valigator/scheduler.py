from __future__ import absolute_import
from docker import Client
from .utils import extract_archive, remove_file
from .notify import MailNotifier
from .celery import app

# TODO: set timeout on tasks


@app.task()
def validate_backup(configuration, backup_data):
    """Celery task.
    It will extract the backup archive into a unique folder
    in the temporary directory specified in the configuration.

    Once extracted, a Docker container will be started and will
    start a restoration procedure. The worker will wait for the
    container to exit and retrieve its return code.
    A notification is sent if the return code is != 0.
    If the return code == 0, the container will be removed.

    Lastly, it will remove the temporary workdir.
    """
    extract_archive(backup_data['archive_path'],
                    backup_data['workdir'])
    docker_client = Client(configuration['docker']['url'])
    container = run_container(docker_client, backup_data)
    return_code = docker_client.wait(container)
    print('Container return code: {}'.format(return_code))
    if return_code != 0:
        notifier = MailNotifier(configuration['mail'])
        report = {'archive': backup_data['archive_path'],
                  'image': backup_data['image'],
                  'container_id': container.get('Id')}
        notifier.send_report(report)
    else:
        docker_client.remove_container(container)
    remove_file(backup_data['workdir'])


def run_container(docker_client, backup_data):
    """Pull the Docker image and creates a container
    with a '/backup' volume. This volume will be mounted
    on the temporary workdir previously created.

    It will then start the container and return the container object.
    """
    docker_client.pull(backup_data['image'])
    container = docker_client.create_container(
        image=backup_data['image'],
        volumes=['/backup'],
        command=backup_data['command'])

    docker_client.start(container.get('Id'), binds={
        backup_data['workdir']:
        {
            'bind': '/backup',
            'ro': False
        }
    })
    return container
