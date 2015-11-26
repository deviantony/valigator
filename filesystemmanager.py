from tarfile import open


class FileSystemManager:

    def extract_archive(self, archive_path, destination_path):
        """Extracts an archive somewhere on the filesystem."""
        tar = open(archive_path, 'r:gz')
        tar.errorlevel = 1
        tar.extractall(destination_path)
