FROM deviantony/python:python2

RUN virtualenv -p /usr/bin/python /env && /env/bin/pip install valigator

CMD ["/env/bin/valigator"]
