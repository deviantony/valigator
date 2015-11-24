#!/bin/sh
exec /sbin/setuser mongodb /usr/bin/mongod --bind_ip 0.0.0.0 >>/var/log/mongodb/mongod.log 2>&1
