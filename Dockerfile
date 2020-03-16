FROM ubuntu:14.04
MAINTAINER zj1244
ENV LC_ALL C.UTF-8
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN set -x \
    && apt-get update \
    && apt-get install python-pip -y \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /opt/beholder_web
COPY . /opt/beholder_web

RUN set -x \
    && pip install -r /opt/beholder_web/requirements.txt \
    && cp /opt/beholder_web/config.env.sample /opt/beholder_web/config.env

WORKDIR /opt/beholder_web
ENTRYPOINT ["python","main.py"]
CMD ["/usr/bin/tail", "-f", "/dev/null"]