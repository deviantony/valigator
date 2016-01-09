valigator
=========

.. epigraph::
    *Check your backups before you wreck yourself !*

|

.. image:: https://readthedocs.org/projects/valigator/badge/?version=latest
  :target: http://valigator.readthedocs.org/en/latest/?badge=latest
  :alt: Documentation Status
.. image:: https://www.quantifiedcode.com/api/v1/project/6b2de325c287407aaf4998cf49c1c09e/badge.svg
  :target: https://www.quantifiedcode.com/app/project/6b2de325c287407aaf4998cf49c1c09e
  :alt: Code issues

|

``valigator`` helps you automate backup validation. It uses *Docker* to create ephemeral environments in which a backup restoration can occur.

It aims to be a generic tool used to test **ANY** backup type. It allows you to use the Docker images that you want and thus, the restoration procedure of your choice.

With ``valigator``, a simple backup procedure now looks like:

- Backup your service
- Trigger a webhook to the ``valigator`` HTTP API
- A backup validation is now queued

Goals
-----

* Ensure valid backups
* Notifications when a restoration test fails

Quick start
-----------

The *entire solution* runs in Docker.

Start a ``rabbitmq`` broker:

.. code-block:: bash

    $ docker run -d --name valigator-broker -p "5672:5672" rabbitmq:latest

Start the ``valigator`` API via a Docker container:

.. code-block:: bash

    $ docker run -d --name valigator-api -p "7000:7000" -v "/path/to/valigator/conf/:/etc/valigator/" valigator/valigator:celery /env/bin/python -m valigator.valigator --conf /etc/valigator/valigator.yml

Start a ``valigator`` worker container:

.. code-block:: bash

    $ sudo docker run -d --name valigator-worker -v "/tmp/valigator:/tmp/valigator" -v "/var/run/docker.sock:/var/run/docker.sock" -v "/path/to/archives/:/path/to/archives/" -v "/etc/valigator/:/etc/valigator/" valigator/valigator:celery /env/bin/celery -A valigator worker --loglevel=info --conf /etc/valigator/valigator.yml

The API is available and a worker is ready, all you need to do is to send a POST query to the API:

.. code-block:: bash

  $ http POST :7000/validate/mongo26 archive_path=/path/to/mongodb/backup/archive.tar.gz

Documentation
-------------

`On readthedocs.org`_ or in the ``docs/source`` directory.

.. _On readthedocs.org: http://valigator.readthedocs.org/en/latest/
