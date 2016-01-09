==========
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

You must restart the `valigator` API/worker components after updating the configuration file.
