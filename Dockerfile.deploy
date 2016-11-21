FROM lambci/lambda-base:build
MAINTAINER Masashi Shibata <contact@c-bata.link>

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LD_LIBRARY_PATH=/lib64:/usr/lib64:/var/runtime:/var/runtime/lib:/var/task:/var/task/lib \
    PYTHONPATH=/var/runtime

RUN rm -rf /var/runtime && \
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python && \
    pip install -U pip virtualenv

RUN yum -y update && \
    yum -y install libjpeg-devel zlib-devel && \
    yum clean all

WORKDIR /app
VOLUME /app/.chalice

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./chalicelib /app/chalicelib
COPY ./app.py /app/app.py
