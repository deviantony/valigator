from docker import Client


class mysql55:

    def __init__(self, configuration):
        self.client = Client(configuration['docker']['socket'])
        self.image = configuration['docker']['images']['mysql55']
        self.mail = configuration['mail']

    def run_container(self, extracted_backup_path):
        command = ''.join([
            '/sbin/my_init -- /usr/local/bin/mysql-check.sh',
            ' -a ', extracted_backup_path,
            ' -s ', self.mail['smtp']['server'],
            ' -u ', self.mail['smtp']['user'],
            ' -p ', self.mail['smtp']['password'],
            ' --mail-to ', self.mail['to_address']])

        container = self.client.create_container(
            image=self.image,
            volumes=['/var/lib/mysql'],
            command=command)

        self.client.start(container.get('Id'), binds={
            extracted_backup_path:
            {
                'bind': '/var/lib/mysql',
                'ro': False
            }
        })
