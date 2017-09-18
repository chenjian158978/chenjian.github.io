FROM ubuntu:14.04
MAINTAINER chenjian "chenjian158978@gmail.com"

# Set the locale
RUN locale-gen zh_CN.UTF-8
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN:zh
ENV LC_ALL zh_CN.UTF-8

# set timezone
RUN echo "Asia/Shanghai" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# 换源
ADD sources.list /
RUN cp /etc/apt/sources.list /etc/apt/sources.list_backup
RUN rm -rf /etc/apt/sources.list
ADD sources.list /etc/apt/sources.list
############################################

RUN apt-get clean
RUN apt-get update
RUN apt-get -y upgrade

RUN apt-get install -y python-dev
RUN apt-get install -y build-essential
RUN apt-get install -y python-pip

ADD librdkafka /librdkafka
WORKDIR /librdkafka
RUN ./configure
RUN make
RUN make install
RUN ldconfig

RUN pip install confluent-kafka

RUN apt-get clean

WORKDIR /
ADD confluentkafka.py /
ADD whilerun.py /
