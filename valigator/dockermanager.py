from docker import Client


class DockerManager:
    """Docker manager.
    Use this object to pull images, create and run containers.
    """

    def __init__(self, configuration):
        self.client = Client(configuration['docker']['socket'])

    def run_container(self, backup_data):
        self.client.pull(backup_data['image'])

        container = self.client.create_container(
            image=backup_data['image'],
            volumes=['/backup'],
            command=backup_data['command'])

        self.client.start(container.get('Id'), binds={
            backup_data['workdir']:
            {
                'bind': '/backup',
                'ro': False
            }
        })

        ret = self.client.wait(container)
        return ret
