FROM alpine:latest
MAINTAINER chenjian chenjian158978@gmail.com

ENV REFRESHED_AT 2016-11-23

RUN apk update \
        && apk --no-cache add curl \
        && curl -sO http://download.redis.io/releases/redis-3.2.5.tar.gz \
        && tar xf redis-3.2.5.tar.gz -C /usr/local/ \
        && rm -rf redis-3.2.5.tar.gz  rm -rf /var/cache/apk/* \
        && cd /usr/local/redis-3.2.5 \
        && apk add --no-cache 'su-exec>=0.2' \
        && apk add --no-cache --virtual .build-deps gcc linux-headers make musl-dev tar \
        && make PREFIX=/usr/local/redis install \
        && apk del .build-deps tar gcc make  \
        && cp utils/redis_init_script /etc/init.d/redis \
        && chmod +x /etc/init.d/redis \
        && sed -i 's@EXEC=/usr/local/bin/redis-server@EXEC=/usr/local/redis/bin/redis-server@' /etc/init.d/redis \
        && sed -i 's@CLIEXEC=/usr/local/bin/redis-cli@CLIEXEC=/usr/local/redis/bin/redis-cli@' /etc/init.d/redis \
        && cd /usr/local \
        && rm -rf /var/cache/apk/* /usr/local/redis-3.2.5
