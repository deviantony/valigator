=============
Configuration
=============

The configuration file *valigator.yml* is written in `YAML format`_.

.. code-block:: yaml

    valigator:
      host: '0.0.0.0'
      port: 7000
      tmp_dir: '/tmp/valigator'

    docker:
      socket: 'unix://var/run/docker.sock'

    celery:
      BROKER_URL: 'amqp://localhost'
      CELERY_TASK_SERIALIZER: 'json'
      CELERY_ACCEPT_CONTENT: ['json']
      CELERY_IMPORTS: ['valigator.scheduler']

    mail:
      from_address: 'automated-backup-test@domain'
      to_address: 'destination-adress@domain'
      title: '[TAG] Backup test failure'
      smtp:
        server: 'smtp.domain'
        port: 25
        timeout: 10
        tls_authentication: True
        user: 'user'
        password: 'pass'

    extension:
      mongo26:
        image: 'mongo:latest'
        command: 'bash -c "mongod --fork --syslog && mongorestore /backup"'


Any change to the configuration file requires a restart of the API/worker components.

Valigator section
=================

This section is related to the component configuration.

``bind``
--------

The server address to bind to.

``port``
--------

The port that will be used to communicate with the component via HTTP.

``tmp_dir``
-----------

Temporary directory in which the backup archives will be extracted.

Docker section
==============

This section is related to the Docker engine.

``url``
--------

The URL of the Docker engine.

Can be either a path to the Docker engine socket or an URL to the Docker API.

Celery section
==============

This section is related to the Celery task queue.

*Note: Celery properties must be written in capital letters.*

``BROKER_URL``
--------------

URL of the broker.

Use `amqp://broker.domain` if you're using RabbitMQ or `redis://broker.domain` if you're using Redis.

For more information on the other properties, have a look at `Celery configuration web page`_.

Mail section
============

This section is related to the e-mail notifications.

``from_address``
----------------

Address from which notification e-mail will be sent.

``to_address``
--------------

Notification will be sent to this address. Does not support multiple e-mail addresses.

``title``
---------

Title of the e-mail.


``smtp.server``
---------------

Address of the SMTP server used to send e-mails.

``smtp.port``
-------------

Port of SMTP server used to send e-mails.

``smtp.timeout``
----------------

Connection timeout to the SMTP server.

``smtp.tls_authentication``
---------------------------

Use TLS authentication with the SMTP server.

``smtp.user``
-------------

If TLS authentication is enabled, use this user to connect to the SMTP server.

``smtp.password``
-----------------

If TLS authentication is enabled, use this password to connect to the SMTP server.

Extension section
=================

This section is related to the Valigator extensions.

See the 'Extensions' chapter for more information on this section.

.. _Celery configuration web page: http://docs.celeryproject.org/en/latest/configuration.html
.. _YAML format: https://en.wikipedia.org/wiki/YAML
