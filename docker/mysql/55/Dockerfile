FROM phusion/baseimage:latest

CMD ["/sbin/my_init"]

RUN apt-get update \
&& apt-get install -y wget mysql-server sendEmail

RUN wget https://github.com/deviantony/common-bash-library/archive/0.1.tar.gz -O cbl.tar.gz \
&& tar xfpvz cbl.tar.gz -C /usr/lib/ \
&& wget https://github.com/deviantony/shflags/archive/1.0.5.tar.gz -O shflags.tar.gz \
&& tar xfpvz shflags.tar.gz -C /usr/lib/ \
&& wget https://github.com/deviantony/bsfl/archive/2.0.1.tar.gz -O bsfl.tar.gz \
&& tar xfpvz bsfl.tar.gz -C /usr/lib/

VOLUME /var/lib/mysql

ADD mysql-check.sh /usr/local/bin/mysql-check.sh
RUN chmod +x /usr/local/bin/mysql-check.sh

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
