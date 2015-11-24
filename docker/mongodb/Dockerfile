FROM phusion/baseimage:latest

CMD ["/sbin/my_init"]

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 \
&& echo 'deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen' | tee /etc/apt/sources.list.d/mongodb-10gen.list \
&& apt-get update \
&& apt-get install -y wget mongodb-10gen=2.6.11 sendEmail

RUN wget https://github.com/deviantony/common-bash-library/archive/0.1.tar.gz -O cbl.tar.gz \
&& tar xfpvz cbl.tar.gz -C /usr/lib/ \
&& wget https://github.com/deviantony/shflags/archive/1.0.5.tar.gz -O shflags.tar.gz \
&& tar xfpvz shflags.tar.gz -C /usr/lib/ \
&& wget https://github.com/deviantony/bsfl/archive/2.0.1.tar.gz -O bsfl.tar.gz \
&& tar xfpvz bsfl.tar.gz -C /usr/lib/

RUN mkdir -pv /data/db

VOLUME /data/db

RUN mkdir /etc/service/mongod
ADD mongod.sh /etc/service/mongod/run
RUN chmod +x /etc/service/mongod/run

ADD mongorestore.sh /usr/local/bin/mongorestore.sh
RUN chmod +x /usr/local/bin/mongorestore.sh

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
