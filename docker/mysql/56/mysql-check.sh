#!/usr/bin/env bash

##
# This script is use to automatically start a MySQL server from a fresh Xtrabackup exploded archive.
# You'll need to explode the backup archive in /var/lib/mysql before lauching the script.
##

HELP_VERSION=1.0.0

## ================================================
## CONSTANTS
## ================================================
MAIL_FROM=automated-backup-test@workit-services.com
MAIL_TITLE="Automated MySQL backup restoration failed"

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
	sendemail -s "${FLAGS_smtp}" -xu "${FLAGS_user}" -xp "${FLAGS_password}" -f "${MAIL_FROM}" -t "${FLAGS_mail_to}" -u "${MAIL_TITLE}" -m "Unable to restore MySQL backup archive: ${FLAGS_archive}"
}

## ================================================
## MAIN
## ================================================

main() {

	chown -R mysql:mysql /var/lib/mysql
	cat /var/lib/mysql/backup-my.cnf >> /etc/mysql/my.cnf
	service mysql start

	mysqladmin ping || send_mail
	RET=$?

	rm -rf /var/lib/mysql/*

	exit ${RET}
}

main
