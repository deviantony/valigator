from __future__ import absolute_import
from celery import Celery
from celery.signals import task_failure
from docker import Client
from traceback import print_tb
from optparse import OptionParser
from celery.bin import Option
from celery.bin.worker import worker
from .utils import remove_file, load_configuration

app = Celery('backups')

# TODO: Refactor
# this section is used to add a --conf option for the worker.
# It allows to read the celery configuration from the YAML file.
app.user_options['worker'].add(
        Option('--conf', action='store', dest='config',
               help='Read configuration from YML configuration file.'),
    )
w = worker(app)
parser = OptionParser(option_list=w.get_options() + w.preload_options)
(options, _) = parser.parse_args()
if options.config:
    config = load_configuration(options.config)
    app.conf.update(config['celery'])


@task_failure.connect
def task_failure_handler(task_id=None, exception=None,
                         traceback=None, args=None, **kwargs):
    """Failure handler"""
    # TODO: find a way to inject notifier in this function
    print('A task failed !')
    print('Taskid: ' + str(task_id))
    print('Args:' + str(args))
    print('Exception: ' + str(exception))
    print('traceback: ' + str(traceback))
    print_tb(traceback)
    # TODO: find a better way to retrieve workdir
    workdir = args[1]['workdir']
    remove_file(workdir)
