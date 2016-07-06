FROM ubuntu:16.04
MAINTAINER Tom Taylor <tom@tommyt.co.uk>

RUN DEBIAN_FRONTEND=noninteractive \
  apt-get -qq update && apt-get -yqq upgrade

RUN DEBIAN_FRONTEND=noninteractive \
  apt-get -yqq install \
    python3 python3-pip python3-numpy python3-scipy python3-matplotlib \
    python3-lxml python3-sqlalchemy python3-iso8601

RUN pip3 install obspy cherrypy
