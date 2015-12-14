from docker import Client


class mysql55_pyxtrabackup:

    def __init__(self, configuration):
        self.client = Client(configuration['docker']['socket'])
        self.image = 'mys56:latest'
        self.mail = configuration['mail']

    def run_container(self, backup_info):
        command = ''.join([
            '/sbin/my_init -- /usr/local/bin/mysql-check.sh',
            ' -a ', backup_info['archive_path'],
            ' -s ', self.mail['smtp']['server'],
            ' -u ', self.mail['smtp']['user'],
            ' -p ', self.mail['smtp']['password'],
            ' --mail-to ', self.mail['to_address'],
            ' --mail-from ', self.mail['from_address']])

        self.client.pull(self.image)

        container = self.client.create_container(
            image=self.image,
            volumes=['/var/lib/mysql'],
            command=command)

        self.client.start(container.get('Id'), binds={
            backup_info['workdir']:
            {
                'bind': '/var/lib/mysql',
                'ro': False
            }
        })
