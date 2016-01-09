=====
Setup
=====

Requirements
============

Docker
------

You'll need to install Docker:

See the `Docker installation web page`_.

*Note: The full solution can be run via Docker, you can skip the other requirements steps.*

Python (optional)
-----------------

If you want to run a part of the solution without Docker, ensure you have Python 2.7.x installed on your system.

You'll need `python-pip`_ to install the solution via `pip` or from sources.

RabbitMQ (optional)
-------------------

A RabbitMQ broker can also be run outside of a Docker engine, see the `RabbitMQ download web page`_ for more information.

Installation
============

The full solution is available via Docker containers, but you can also install it on your system.

From pypi
---------

Use ``pip`` to install it:

.. code-block:: bash

   $ pip install valigator

This will install the default configuration file in */etc/valigator/valigator.yml*.

From sources
------------

Clone the repository:

.. code-block:: bash

  $ git clone https://github.com/deviantony/valigator.git
  $ cd valigator && pip install -r requirements.txt


.. _Docker installation web page: https://docs.docker.com/engine/installation/
.. _python-pip: https://pip.pypa.io/en/stable/installing/
.. _RabbitMQ download web page: https://www.rabbitmq.com/download.html
