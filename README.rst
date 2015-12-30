valigator
=========

.. epigraph::
    *Check your backups before you wreck yourself !*

|

.. image:: https://www.quantifiedcode.com/api/v1/project/6b2de325c287407aaf4998cf49c1c09e/badge.svg
  :target: https://www.quantifiedcode.com/app/project/6b2de325c287407aaf4998cf49c1c09e
  :alt: Code issues

|

| ``valigator`` helps you automate backup validation. It uses *Docker* to create ephemeral environments in which a backup restoration can occur.

| It aims to be a generic tool used to test **ANY** backup type:
| - Database backup (*mysql*, *mongodb*...)
| - ...

Introduction
============

The solution is composed of 2 components : the ``valigator`` API service and one or more ``valigator`` worker.

Both components use a broker to communicate.

.. image:: https://www.lucidchart.com/publicSegments/view/8e361ed5-92d4-4100-81a4-874cccfd085d/image.jpeg

Valigator HTTP API
------------------

The HTTP API component exposes an endpoint used to register backup testing tasks in the broker. These task will be executed by the *worker* component.

``/validate/<backup>``
~~~~~~~~~~~~~~~~~~~~~~

Register a new backup test task, it will use the *<backup>* parameter to choose which extension to load.

It only support the POST method.

When hitting the endpoint with a POST, it expects a JSON request body that must look like:

.. code-block:: javascript

    {
      "archive_path": "/path/to/archive"
    }


The *archive_path* field is mandatory, it specifies the location on the filesystem where the tool can find the backup archive.

Example, plan a MongoDB 2.6 backup test for the archive located at /path/to/mongodb/backup/archive.tar.gz:

.. code-block:: bash

  $ http POST :7000/validate/mongo26 archive_path=/path/to/mongodb/backup/archive.tar.gz


Valigator worker
----------------

A worker subscribes to the broker and will trigger backup test in Docker container when it receives a task.

Basically, a worker will start a Docker container using a specific command with a `/backup` mount point containing the exploded backup archive.

The return code of the command used to validate the backup will trigger a notification if different from 0.

Installation
============

Requirements
------------

Docker
~~~~~~

You'll need to install Docker:

See the `Docker installation web page`_.

*Note*: The full solution can be run via Docker, you can skip the other requirements steps.

Python (optional)
~~~~~~~~~~~~~~~~~

If you want to run a part of the solution without Docker, ensure you have Python 2.7.x installed on your system.

You'll need `python-pip`_ to install the solution via `pip` or from sources.

RabbitMQ (optional)
~~~~~~~~~~~~~~~~~~~

A RabbitMQ broker can also be run outside of a Docker engine, see the `RabbitMQ download web page`_ for more information.

Setup
-----

The full solution is available via Docker containers, but you can also install it via classic ways.

From pypi
~~~~~~~~~

Use ``pip`` to install it::

   $ pip install valigator

This will install the default configuration file in */etc/valigator/valigator.yml*.

From sources
~~~~~~~~~~~~

Clone the repository::

  $ git clone https://github.com/deviantony/valigator.git
  $ cd valigator && pip install -r requirements.txt

Usage
=====

Start the solution using Docker
-------------------------------

Start a ``rabbitmq`` broker::

    $ docker run -d --name valigator-broker -p "5672:5672" rabbitmq:latest

Start the ``valigator`` API via a Docker container::

    $ docker run -d --name valigator-api -p "7000:7000" -v "/path/to/valigator/conf/:/etc/valigator/" valigator/valigator:celery /env/bin/python -m valigator.valigator --conf /etc/valigator/valigator.yml

Start a ``valigator`` worker container::

    $ sudo docker run -d --name valigator-worker -v "/tmp/valigator:/tmp/valigator" -v "/var/run/docker.sock:/var/run/docker.sock" -v "/path/to/archives/:/path/to/archives/" -v "/etc/valigator/:/etc/valigator/" valigator/valigator:celery /env/bin/celery -A valigator worker --loglevel=info --conf /etc/valigator/valigator.yml

By default, a worker container will execute tasks concurrently, you can change the number of worker processes/threads using the `--concurrency` option (default value equals to number of available CPUs).

Start a ``valigator`` worker container and limit its processes to 2::

  $ sudo docker run -d --name valigator-worker -v "/tmp/valigator:/tmp/valigator" -v "/var/run/docker.sock:/var/run/docker.sock" -v "/path/to/archives/:/path/to/archives/" -v "/etc/valigator/:/etc/valigator/" valigator/valigator:celery /env/bin/celery -A valigator worker --loglevel=info --conf /etc/valigator/valigator.yml --concurrency 2

Start the solution without Docker
---------------------------------

Ensure you got a running RabbitMQ broker before trying to start the ``valigator`` components:

If installed via pip, use the binary to run the ``valigator`` API::

    $ valigator --conf /path/to/valigator/conf/file

If installed from source, execute the module::

    $ python -m valigator.valigator --conf /path/to/valigator/conf/file

To start the ``valigator`` worker, use the `celery` binary::

    $ celery worker -A valigator worker --loglevel=info --conf /path/to/valigator/conf/file

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


Valigator section
-----------------

This section is related to the component configuration.

``bind``
~~~~~~~~

The server address to bind to.

``port``
~~~~~~~~

The port that will be used to communicate with the component via HTTP.

``tmp_dir``
~~~~~~~~~~~

Temporary directory in which the backup archives will be extracted.

Docker section
--------------

This section is related to the Docker engine.

``url``
~~~~~~~~

The URL of the Docker engine.

Can be either a path to the Docker engine socket or an URL to the Docker API.

Celery section
--------------

This section is related to the Celery task queue.

*Note*: Celery properties must be written in capital letters.

``BROKER_URL``
~~~~~~~~~~~~~~

URL of the broker.

Use `amqp://broker.domain` if you're using RabbitMQ or `redis://broker.domain` if you're using Redis.

For more information on the other properties, have a look at `Celery configuration web page`_.

Mail section
------------

This section is related to the e-mail notifications.

``from_address``
~~~~~~~~~~~~~~~~

Address from which notification e-mail will be sent.

``to_address``
~~~~~~~~~~~~~~

Notification will be sent to this address. Does not support multiple e-mail addresses.

``smtp.server``
~~~~~~~~~~~~~~~

Address of the SMTP server used to send e-mails.

``smtp.port``
~~~~~~~~~~~~~

Port of SMTP server used to send e-mails.

``smtp.timeout``
~~~~~~~~~~~~~~~~

Connection timeout to the SMTP server.

``smtp.tls_authentication``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use TLS authentication with the SMTP server.

``smtp.user``
~~~~~~~~~~~~~

If TLS authentication is enabled, use this user to connect to the SMTP server.

``smtp.password``
~~~~~~~~~~~~~~~~~

If TLS authentication is enabled, use this password to connect to the SMTP server.

Extension section
-----------------

This section is related to the Valigator extensions.

See the 'Extensions' chapter below for more information on this section.

Extensions
==========

Valigator is using an extension system that allows you to test your backups using any Docker image.

To register an extension, edit the *valigator.yml* configuration file and add a block under the extension section with two properties: *image* and *command*.

For example, add a section to test backup for MySQL 5.6:

.. code-block:: yaml

    extension:
      mysql56:
        image: 'mysql:5.6'
        command: 'cat /backup/*.sql | mysql -u root'

You'll be able to plan backup tests by sending a POST request to `http://valigator-api.domain:7000/validate/mysql56`.

Limitations
===========

This tool has been tested on the following OSes:

* Ubuntu 14.04

It has been tested against the following Python versions:

* Python 2.7

.. _Docker installation web page: https://docs.docker.com/engine/installation/
.. _python-pip: https://pip.pypa.io/en/stable/installing/
.. _RabbitMQ download web page: https://www.rabbitmq.com/download.html
.. _Celery configuration web page: http://docs.celeryproject.org/en/latest/configuration.html
.. _YAML format: https://en.wikipedia.org/wiki/YAML
