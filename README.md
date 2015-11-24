# backup-validator

> Check your backups before you wreck yourself !

Use Docker to perform database backup validation.

This exposes an API to trigger a backup restoration inside a Docker container.

Supported databases:

* MongoDB
* MySQL (5.5/5.6)


## Setup

Ensure you have Python >= 3.4 installed on your machine.

Install the following dependencies:

```bash
$ sudo pip install -r requirements.txt
```

## Docker images

You'll need to build the Docker images:

```bash
$ docker build -t my_mongodb26 docker/mongodb
$ docker build -t my_mysql55 docker/mysql/55
```

Do not forget to update the *settings.py* file after changing the images name.

## Usage

Start the API:

```bash
$ sudo python backuptestapi.py
```

## Endpoints

### /backup/mysql

Use this endpoint to start a restoration test against a MySQL backup archive.

It expects a JSON request body to be POST. The request body must look something like:

```json
{
    "archive_path": "/path/to/backup/archive",
}
```

*NOTE*: the archive must accessible on the filesystem.

### /backup/mongodb

Use this endpoint to start a restoration test against a MongoDB backup archive.

It expects a JSON request body to be POST. The request body must look something like:

```json
{
    "archive_path": "/path/to/backup/archive",
}
```

*NOTE*: the archive must accessible on the filesystem.

## Notifications

A notification of failure is sent in the following cases:

* An error occured during the archive extraction
* An error occured during the restoration phasis
