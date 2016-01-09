=======
Reports
=======

A report is sent via e-mail if a worker task fails or if a backup container returns a code != 0.

These will help you diagnose the issue.

Task failure
============

Available fields:

- Error: Error summary.

- Task ID: Celery task ID.

- Archive: Path to the tested backup archive.

- Docker image: Associated Docker image.

- Traceback: The Python stack trace.

Report example:

.. code-block:: text

  Error: task failure

  Task ID: b2105add-5e5f-43ec-8e65-94ddd1b49658

  Archive: /tmp/corrupted_archive.tar.gz

  Docker image: mongo:2.6

  Exception: file could not be opened successfully

  Traceback:
   File "/env/lib/python2.7/site-packages/celery/app/trace.py", line 240, in trace_task
    R = retval = fun(*args, **kwargs)
  File "/env/lib/python2.7/site-packages/celery/app/trace.py", line 438, in __protected_call__
    return self.run(*args, **kwargs)
  File "/app/valigator/scheduler.py", line 25, in validate_backup
    backup_data['workdir'])
  File "/app/valigator/utils.py", line 24, in extract_archive
    tar = tarfile.open(archive_path)
   File "/usr/lib/python2.7/tarfile.py", line 1672, in open
    raise ReadError("file could not be opened successfully")


Backup test failure
===================

Available fields:

- Error: Error summary.

- Archive: Path to the tested backup archive.

- Docker image: Associated Docker image.

- Docker container: ID of the Docker container in failure state (use it to display the logs of the container).

Report example:

.. code-block:: text

  Error: return code != 0

  Archive: /tmp/valid_archive.tar.gz

  Docker image: mongo:2.6

  Docker container: d78cb5ef29ea1c3c06d176089ec7a36e564419634f921d31a4130f8478f23e69
