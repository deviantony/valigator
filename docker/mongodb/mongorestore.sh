#!/usr/bin/env bash

##
# This script is use to automatically load a mongodump backup.
# It will try to load the data for a database stored in /tmp/backup.
# You'll need to explode the backup archive in /tmp/backup before lauching the script.
# Example of use: docker run --rm -it -v /tmp/backup/BACKUP-UUID:/tmp/backup mongo-wit /sbin/my_init -- /usr/local/bin/mongorestore.sh pim
##

HELP_VERSION=1.0.0

## ================================================
## CONSTANTS
## ================================================
MAIL_FROM=automated-backup-test@workit-services.com
MAIL_TITLE="Automated MongoDB backup restoration failed"
MONGODB_PORT=27017

## ================================================
## LIBRARIES
## ================================================
SHFLAGS_LIB_PATH=/usr/lib/workit/bash-libraries/shflags
BSFL_LIB_PATH=/usr/lib/workit/bash-libraries/bsfl
CBL_LIB_PATH=/usr/lib/workit/bash-libraries/cbl

source ${CBL_LIB_PATH}
if [[ $? -ne 0 ]]; then
  echo "Unable to source cbl library: ${CBL_LIB_PATH}"
  exit ${_EXEC_FAILURE}
fi

source ${BSFL_LIB_PATH}
if [[ $? -ne 0 ]]; then
  echo "Unable to source bsfl library: ${BSFL_LIB_PATH}"
  exit ${_EXEC_FAILURE}
fi

source ${SHFLAGS_LIB_PATH}
if [[ $? -ne 0 ]]; then
  echo "Unable to source shFlags library: ${SHFLAGS_LIB_PATH}"
  exit ${_EXEC_FAILURE}
fi

## ================================================
## FLAGS
## ================================================
DEFINE_string 'archive' '' 'Archive path' 'a' 'required'
DEFINE_string 'smtp' '' 'SMTP server' 's' 'required'
DEFINE_string 'user' '' 'SMTP user' 'u' 'required'
DEFINE_string 'password' '' 'SMTP password' 'p' 'required'
DEFINE_string 'mail-to' 'service_exploitation@workit.fr' 'to email addresses (space separated)'

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"


## ================================================
## BSFL
## LOG_ENABLED: Enable/disable the logging via BSFL.
## LOG_FILE: Where to log messages. You should define a flag to specify the log file path.
## ================================================
LOG_ENABLED=y
LOG_FILE=${FLAGS_log_file}

## ================================================
## METHODS
## ================================================
###################################################
# Send an email linking the file /tmp/mongorestore.log
# as an attached document.
function send_mail() {
	sendemail -s "${FLAGS_smtp}" -xu "${FLAGS_user}" -xp "${FLAGS_password}" -f "${MAIL_FROM}" -t "${FLAGS_mail_to}" -u "${MAIL_TITLE}" -m "Unable to restore MySQL backup archive: ${FLAGS_archive}" -a /tmp/mongorestore.log
}

## ================================================
## MAIN
## ================================================

main() {

	chown -R mongodb:mongodb /data/db

	RET=1
	while [[ RET -ne 0 ]]; do
	    echo "=> Waiting for confirmation of MongoDB service startup"
	    sleep 5
	    mongo admin --eval "help" >/dev/null 2>&1
	    RET=$?
	done

	mongorestore --host localhost --port ${MONGODB_PORT} --drop /tmp/backup > /tmp/mongorestore.log 2>&1

	grep "ERROR" /tmp/mongorestore.log && send_mail

	rm -rf /tmp/backup/*
	rm -rf /data/db/*

	exit ${_EXEC_SUCCESS}
}

main
