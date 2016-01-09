Valigator documentation
=======================

``valigator`` helps you automate backup validation.

It uses *Docker* to create ephemeral environments in which a backup restoration can occur.

It aims to be a generic tool used to test **ANY** backup type. It allows you to use the Docker images that you want and thus, the restoration procedure of your choice.

Table of content
================

.. toctree::
   :maxdepth: 2

   setup
   configuration
   usage
   extensions
   reports
   maintenance
   limitations

The solution is composed of 2 components : the ``valigator`` HTTP API service and one or more ``valigator`` worker.

Both components use a broker to communicate.

.. image:: https://www.lucidchart.com/publicSegments/view/8e361ed5-92d4-4100-81a4-874cccfd085d/image.jpeg

Valigator HTTP API
------------------

This component is the front service of ``valigator``, use it to queue backup tasks. These tasks will be executed by the *worker* component.

The HTTP API component exposes one endpoint.

``/validate/<backup>``
~~~~~~~~~~~~~~~~~~~~~~

Use this endpoint to queue a new backup test task, it will use the *<backup>* parameter to choose which extension to load (see the Extensions chapter for more info).

It only support the POST method.

When hitting the endpoint with a POST, it expects a JSON request body that must look like:

.. code-block:: javascript

    {
      "archive_path": "/path/to/archive"
    }


The *archive_path* field is mandatory, it specifies the location on the filesystem where the tool can find the backup archive.

Example, plan a MongoDB 2.6 backup test for the archive located at /path/to/mongodb/backup/archive.tar.gz (using `HTTPie`_ to send the request):

.. code-block:: bash

  $ http POST :7000/validate/mongo26 archive_path=/path/to/mongodb/backup/archive.tar.gz


Valigator worker
----------------

A worker subscribes to the broker and will trigger backup test in Docker container when it receives a task. You can have more than one worker (even on multiple Docker engines).

A worker task consists of the following:

- Extract the backup archive in a temporary directory
- Start a Docker container based on the extension image, it will also mount the temporary directory containing the exploded backup to the */backup* folder.
- Execute the command specified in the extension

*NOTE*: The worker must have access to the archive on the filesystem.

The return code of the command used to validate the backup will trigger a notification if different from 0.
A notification is also triggered if any exception occurs during the task.

.. _HTTPie: https://github.com/jkbrzt/httpie
