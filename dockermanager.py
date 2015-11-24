from docker import Client


class DockerManager:

    def __init__(self, docker_configuration, mail_configuration):
        self.client = Client(docker_configuration["socket"])
        self.images = docker_configuration["images"]
        self.mail = mail_configuration

    # Generic method, should be able to start a validation container
    # for mysql 55/56 & mongodb
    def run_container():
        pass

    def run_mysql_container(self, backup_path, archive_path, mysql_version):
        """ Run a MySQL container with appropriate volumes
        and start the archive restoration test.
        Depending on the specified MySQL version a specific MySQL container
        will be used.

        A volume is mapped from the Docker engine filesystem where
        the exploded backup is located to the /var/lib/mysql folder
        in the container.
        """
        command = ''.join([
            '/sbin/my_init -- /usr/local/bin/mysql-check.sh',
            ' -a ', archive_path,
            ' -s ', self.mail["smtp"]["server"],
            ' -u ', self.mail["smtp"]["user"],
            ' -p ', self.mail["smtp"]["password"],
            ' --mail-to ', self.mail["to_address"]])

        if mysql_version == '5.5':
            image = self.images["MySQL_55"]
        elif mysql_version == '5.6':
            image = self.images["MySQL_56"],

        container = self.client.create_container(
            image=image,
            volumes=['/var/lib/mysql'],
            command=command)

        self.client.start(container.get('Id'), binds={
            backup_path:
            {
                'bind': '/var/lib/mysql',
                'ro': False
            }
        })

    def run_mongo_container(self, backup_path, archive_path, db_path):
        """ Run a MongoDB container with appropriate volumes
        and start the archive restoration test.

        One volume is mapped from the Docker engine filesystem where
        the backup archive is located to the /tmp/backup folder
        in the container.
        Another volume is mapped from the Docker engine filesystem
        (a temporary workdir) to the /data/db folder in the container.
        """
        command = ''.join([
            '/sbin/my_init -- /usr/local/bin/mongorestore.sh',
            ' -a ', archive_path,
            ' -s ', self.mail["smtp"]["server"],
            ' -u ', self.mail["smtp"]["user"],
            ' -p ', self.mail["smtp"]["password"],
            ' --mail-to ', self.mail["to_address"]])
        container = self.client.create_container(image=self.images["MongoDB"],
                                                 volumes=['/tmp/backup',
                                                 '/data/db'],
                                                 command=command)

        self.client.start(container.get('Id'), binds={
            backup_path:
            {
                'bind': '/tmp/backup',
                'ro': False
            },
            db_path:
            {
                'bind': '/data/db',
                'ro': False
            },
        })
