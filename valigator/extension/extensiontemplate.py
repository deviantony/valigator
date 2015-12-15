from docker import Client


class extensionTemplate(object):
    """ Extension template.
    Create your Docker container specific to your backup restoration
    in this class.
    """
    def __init__(self, configuration):
        self.client = Client(configuration['docker']['socket'])
        self.image = 'my_docker_image:latest'
        self.mail = configuration['mail']

    def run_container(self, backup_info):
        """Initialize and run your container in this section"""
        print(backup_info)
        pass
