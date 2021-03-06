import base64
import uuid
import tarfile
from shutil import rmtree
from os import path
from yaml import safe_load


def generate_uuid():
    """Generate a UUID."""
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return r_uuid.decode().replace('=', '')


def load_configuration(configuration_file):
    """Load the configuration object from the configuration file."""
    with open(configuration_file, 'r') as stream:
        config = safe_load(stream)
        return config


def extract_archive(archive_path, destination_path):
    """Extracts an archive somewhere on the filesystem."""
    tar = tarfile.open(archive_path)
    tar.errorlevel = 1
    tar.extractall(destination_path)


def remove_file(file_path):
    """Remove a file from the filesystem."""
    if path.exists(file_path):
        try:
            rmtree(file_path)
        except Exception:
            print('Unable to remove temporary workdir {}'.format(file_path))
