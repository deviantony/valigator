from docker import Client


class mongo26:

    def __init__(self, configuration):
        self.client = Client(configuration['docker']['socket'])
        self.image = configuration['docker']['images']['mongodb26']
        self.mail = configuration['mail']

    def run_container(self, extracted_backup_path):
        command = ''.join([
            '/sbin/my_init -- /usr/local/bin/mongorestore.sh',
            ' -a ', extracted_backup_path,
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
