from __future__ import absolute_import
from celery import Celery
from celery.signals import task_failure
from optparse import OptionParser
from celery.bin import Option
from celery.bin.worker import worker
from .utils import remove_file, load_configuration
from .notify import MailNotifier

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
    notifier = MailNotifier(config['mail'])


@task_failure.connect
def task_failure_handler(task_id=None, exception=None,
                         traceback=None, args=None, **kwargs):
    """Task failure handler"""
    # TODO: find a better way to acces workdir/archive/image
    task_report = {'task_id': task_id,
                   'exception': exception,
                   'traceback': traceback,
                   'archive': args[1]['archive_path'],
                   'image': args[1]['image']}
    notifier.send_task_failure_report(task_report)
    workdir = args[1]['workdir']
    remove_file(workdir)
