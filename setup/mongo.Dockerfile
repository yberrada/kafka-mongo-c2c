FROM mongo:6.0.5
COPY config-replica.js /
COPY .bashrc /data/db/.bashrc
COPY requirements.txt /

RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y curl

RUN mkdir -p /home/c2c
ADD sink_connector /home/sink_connector
ADD app /home/app
RUN curl https://fastdl.mongodb.org/tools/mongosync/mongosync-ubuntu2004-x86_64-1.7.1.tgz -o mongosync-ubuntu.tgz
RUN mv mongosync-ubuntu.tgz /home/c2c
RUN cd home/c2c && tar -zxvf mongosync-ubuntu.tgz
RUN cp /home/c2c/mongosync-ubuntu2004-x86_64-1.7.1/bin/mongosync /usr/local/bin/

ADD utils /usr/local/bin
RUN chmod +x /usr/local/bin/cx
RUN chmod +x /usr/local/bin/del
RUN chmod +x /usr/local/bin/kc
RUN chmod +x /usr/local/bin/status

RUN apt-get install -y python3-pip
RUN apt-get install -y nano
RUN apt-get install -y bsdmainutils
RUN apt-get install -y kafkacat
RUN apt-get install -y git
RUN apt-get install -y dos2unix

RUN dos2unix /usr/local/bin/*
RUN dos2unix /data/db/.bashrc
RUN pip3 install -r /requirements.txt
