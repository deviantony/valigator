=====
Usage
=====

Start the solution using Docker
===============================

Start a ``rabbitmq`` broker:

.. code-block:: bash

    $ docker run -d --name valigator-broker -p "5672:5672" rabbitmq:latest

Start the ``valigator`` API via a Docker container:

.. code-block:: bash

    $ docker run -d --name valigator-api -p "7000:7000" -v "/path/to/valigator/conf/:/etc/valigator/" valigator/valigator:celery /env/bin/python -m valigator.valigator --conf /etc/valigator/valigator.yml

You'll need to pass the following volumes:

- Mount your local configuration folder to */etc/valigator* (can be changed via the *--conf* option)

Start a ``valigator`` worker container:

.. code-block:: bash

    $ sudo docker run -d --name valigator-worker -v "/tmp/valigator:/tmp/valigator" -v "/var/run/docker.sock:/var/run/docker.sock" -v "/path/to/archives/:/path/to/archives/" -v "/path/to/valigator/conf/:/etc/valigator/" valigator/valigator:celery /env/bin/celery -A valigator worker --loglevel=info --conf /etc/valigator/valigator.yml

You'll need to pass the following volumes:

- Mount the temporary directory specified in the configuration file (use the same mount point in the container)
- Mount the local Docker socket (use the same mount point in the container)
- Mount the backup repository (use the same mount point in the container)
- Mount your local configuration folder to */etc/valigator* (can be changed via the *--conf* option)

By default, a worker container will execute tasks concurrently, you can change the number of worker processes/threads using the `--concurrency` option (default value equals to number of available CPUs).

Start a ``valigator`` worker container and limit its processes to 2:

.. code-block:: bash

  $ sudo docker run -d --name valigator-worker -v "/tmp/valigator:/tmp/valigator" -v "/var/run/docker.sock:/var/run/docker.sock" -v "/path/to/archives/:/path/to/archives/" -v "/path/to/valigator/conf/:/etc/valigator/" valigator/valigator:celery /env/bin/celery -A valigator worker --loglevel=info --conf /etc/valigator/valigator.yml --concurrency 2

Start the solution without Docker
=================================

Ensure you got a running RabbitMQ broker before trying to start the ``valigator`` components:

If installed via pip, use the binary to run the ``valigator`` API:

.. code-block:: bash

    $ valigator --conf /path/to/valigator/conf/file

If installed from source, execute the module:

.. code-block:: bash

    $ python -m valigator.valigator --conf /path/to/valigator/conf/file

To start the ``valigator`` worker, use the `celery` binary:

.. code-block:: bash

    $ celery worker -A valigator worker --loglevel=info --conf /path/to/valigator/conf/file
