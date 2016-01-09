===========
Maintenance
===========

Docker seems to keep orphaned volumes on the filesystem even if the container has been removed.

To resolve this problem, I use the following script scheduled on a daily basis: https://github.com/chadoe/docker-cleanup-volumes

Plan it inside a cron file (example, every day at midnight):

.. code-block:: bash

    @midnight 	root	docker run -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/docker:/var/lib/docker --rm martin/docker-cleanup-volumes
