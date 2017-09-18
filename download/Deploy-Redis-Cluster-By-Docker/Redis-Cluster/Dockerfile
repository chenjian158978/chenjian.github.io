FROM redis_base:latest
MAINTAINER chenjian chenjian158978@gmail.com

ADD redis-6379.conf /usr/local/redis/bin/redis-6379.conf
ADD redis-6380.conf /usr/local/redis/bin/redis-6380.conf
ADD redis-6381.conf /usr/local/redis/bin/redis-6381.conf
ADD redis-6382.conf /usr/local/redis/bin/redis-6382.conf
ADD redis-6383.conf /usr/local/redis/bin/redis-6383.conf
ADD redis-6384.conf /usr/local/redis/bin/redis-6384.conf
ADD start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]
