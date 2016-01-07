from __future__ import absolute_import
import click
from bottle import post, run, request, abort
from .utils import generate_uuid, load_configuration
from .scheduler import validate_backup
from .celery import app


@post('/validate/<backup>')
def validate(backup):
    """Use this endpoint to start a backup validation.
    You must specify the backup type in the endpoint.
    Specify JSON data for backup archive info.

    {
        'archive_path': '/path/to/archive'
    }

    Data must be valid, otherwise it will abort with a 400 code.

    First, it will try to search for an existing extension definition
    in the configuration file. If no matching extension is found, it
    will abort with a 404 code.

    It will then plan the backup validation by sending a message
    to the broker.
    """
    data = request.json
    if not data:
        abort(400, 'No data received')

    try:
        archive_path = data['archive_path']
    except KeyError:
        abort(400, 'Missing key \'archive_path\' in data')

    try:
        config['extension'][backup]
    except KeyError:
        abort(404, 'No extension configuration found for: {}'.format(backup))

    workdir = ''.join([config['valigator']['tmp_dir'], '/', generate_uuid()])
    backup_data = {'archive_path': archive_path,
                   'workdir': workdir,
                   'image': config['extension'][backup]['image'],
                   'command': config['extension'][backup]['command']}
    validate_backup.delay(config, backup_data)


@click.command()
@click.option('--conf', default='/etc/valigator/valigator.yml',
              help='Valigator configuration file',
              show_default=True)
def main(conf):
    """Main function, entry point of the program."""
    global config
    config = load_configuration(conf)
    app.conf.update(config['celery'])
    run(host=config['valigator']['bind'], port=config['valigator']['port'])

if __name__ == '__main__':
    main()
