---
layout:     post
title:      "Kubernetes集群之Kafka和ZooKeeper"
subtitle:   "Deploy Kafka And ZP With K8s"
date:       Wed, Apr 11 2017 16:01:18 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Kafka-And-ZP-With-K8s/head_blog.jpg"
catalog:    true
tags: [工作, Kubernetes]
---

### 系列博文

- [在Linux上使用Kubeadm工具部署Kubernetes](https://o-my-chenjian.com/2016/12/08/Deploy-K8s-by-Kubeadm-on-Linux/)
- [带你玩转Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Kubernetes集群之搭建ETCD集群](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Kubernetes集群之Dashboard](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)
- [Kubernetes集群之Monitoring](https://o-my-chenjian.com/2017/04/08/Deploy-Monitoring-With-K8s/)
- [Kubernetes集群之Logging](https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/)
- [Kubernetes集群之Ingress](https://o-my-chenjian.com/2017/04/08/Deploy-Ingress-With-K8s/)
- [Kubernetes集群之Redis Sentinel集群](https://o-my-chenjian.com/2017/02/06/Deploy-Redis-Sentinel-Cluster-With-K8s/)
- [Kubernetes集群之Kafka和ZooKeeper](https://o-my-chenjian.com/2017/04/11/Deploy-Kafka-And-ZP-With-K8s/)

### Github

依据[Yolean/kubernetes-kafka](https://github.com/Yolean/kubernetes-kafka)

### 镜像和Yaml文件

可以在[这里](https://pan.baidu.com/s/1pLhmqzL)进行下载tar包和yaml文件

当前使用的版本：

- kafka 2.11-0.10.1.1
- zookeeper 3.4.9


### 分布部署

##### 创建命名空间

`kubectl create -f namespace.yaml`

##### 创建PV和PVC

``` bash
kubectl create -f pv.yaml
kubectl create -f pvc.yaml
```

先pv后pvc，通过`kubectl get pv`可以看见三个pv已被**Bound**。

注意：

- pv路径在`/tmp/kafka-data/`下。当服务器重启后，`/tmp`文件夹会被清空；

- pv与pvc的storeage需要注意；

- 使用的是hostPath，可以改用为NFS。官方告知
	- `single node testing only – local storage is not supported in any way and WILL NOT WORK in a multi-node cluster`

- 需要对kafka的类型`StatefulSet`熟悉

##### 搭建ZooKeeper

``` bash
kubectl create -f zookeeper/
```

注意：

`terminationGracePeriodSeconds：60`， 这个参数可以优雅的每隔60s开启一个容器 

##### 搭建Kafka

``` bash
kubectl create -f zookeeper/
```

##### 创建topics

``` bash
kubectl create -f createTopics/topic-create.yaml
```

其中使用的类型是**Job**，即一次性运行成功即可。

在pv的数据存储路径下`/tmp/kafka-data/`下面可以看到创建的topics。

**但是当你失去整个zookeeper集群时，kafka集群将不知晓已存在的topic，即使数据仍然存在，但是还需再次创建topics**


### python连接Kafka/ZP

##### Dockerfile

没玩过**Docker**，来看[Easy With Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)吧！

代码下载：[Dockerfile](/download/Deploy-Kafka-And-ZP-With-K8s/Dockerfile)

``` docker
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
```

##### whilerun.py

代码下载：[whilerun.py](/download/Deploy-Kafka-And-ZP-With-K8s/whilerun.py)

为保证容器后台有一直运行的程序

``` python
# -*- coding:utf8 -*-

"""
@author: chenjian158978@gmail.com

@date: Thu, Apr 20 2017

@time: 15:20:08 GMT+8
"""
import time
from datetime import datetime


def main():
    while 1:
        print datetime.now()
        time.sleep(60)


if __name__ == '__main__':
    main()
```

##### zpkafka.yaml

代码下载：[zpkafka.yaml](/download/Deploy-Kafka-And-ZP-With-K8s/zpkafka.yaml)

``` yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: zpkafka
  namespace: kafka
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: zpkafka
    spec:
      containers:
        - name: zpkafka
          image: zpkafka:test
          command:
            - "python"
            - "whilerun.py" 
```

- 注意namespace要和kafka相同

##### confluentkafka.py

代码下载：[confluentkafka.py](/download/Deploy-Kafka-And-ZP-With-K8s/confluentkafka.py)

``` python
# -*- coding:utf8 -*-

"""
Using confluent-kafka

@author: chenjian158978@gmail.com

@date: Wed, Nov 23

@time: 11:39:30 GMT+8
"""

from confluent_kafka import Producer
from confluent_kafka import Consumer, KafkaError, KafkaException


class TestConfluentKafka(object):
    def __init__(self):
        self.broker = 'kafka:9092'
        self.group_id = 'vul_test'
        self.topic_con = ['vul_test']
        self.topic_pro = 'vul_test'

    def test_producer(self):
        """ 消息生产者
        
        """
        conf = {'bootstrap.servers': self.broker}

        p = Producer(**conf)
        some_data_source = [
            "chennnnnnnnnnnnnnnnnnnnnn",
            "jiansssssssssssssssssss",
            "hellossssssssssssssss",
            "dddddddddddddddddddddddd"]
        for data in some_data_source:
            p.produce(self.topic_pro, data.encode('utf-8'))

        p.flush()

    def test_consumer(self):
        """ 消息消费者
        
        """
        conf = {'bootstrap.servers': self.broker,
                'group.id': self.group_id,
                'default.topic.config': {'auto.offset.reset': 'smallest'}}

        c = Consumer(**conf)
        c.subscribe(self.topic_con)

        try:
            while True:
                msg = c.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print msg.topic(), msg.partition(), msg.offset()
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    print '%% %s [%d] at offset %d with key %s:\n' \
                          % (msg.topic(),
                             msg.partition(),
                             msg.offset(),
                             str(msg.key()))
                    print msg.value()
        except KeyboardInterrupt:
            print '%% Aborted by user\n'

        finally:
            c.close()


if __name__ == '__main__':
    #TestConfluentKafka().test_producer()
    TestConfluentKafka().test_consumer()
```

- 注意：
	- 采用第三方库confluent-kafka，可以尝试换用其他库
	- 在配置里面的topics，要和之前插入的topics相同。这个建议改用环境变量形式，在yaml中加入env即可
	- 方法test_producer()是信息生产者，方法test_consumer()是消息消费者

#### nodejs连接Kafka/ZP

代码下载：[connectKafka.js](/download/Deploy-Kafka-And-ZP-With-K8s/connectKafka.js)

``` javascript
/**
 * Created by jianchan on 21/04/2017.
 */

var kafka = require('kafka-node');
var util = require('util');
var moment = require('moment');

var params = {'zookeeper_connec': 'zookeeper:2181'};
var topics = {'abc': 'abc_test'};
var groupId = {'abc': 'abc_test'};


var Client = kafka.Client;
var KeyedMessage = kafka.KeyedMessage;
var HighLevelProducer = kafka.HighLevelProducer;
var HighLevelConsumer = kafka.HighLevelConsumer;

var client = new Client(params.zookeeper_connec);

// 消息生产者
var producer = new HighLevelProducer(client);
var data = {
    "data": "dddddddxxxxxx"
};

producer.on('ready', function () {
    var timeSpan = Date.now();
    var sendData = JSON.stringify(data.data);
    send(topics.abc, timeSpan, sendData);
});

producer.on('error', function (err) {
    console.log(err);
});

function send(topic, key, value) {
    if (!util.isString(key)) {
        key = key.toString();
    }
    var keyedMessage = new KeyedMessage(key, value);
    producer.send([{topic: topic, messages: [keyedMessage]}],
        function (err, data) {
            if (err) {
                console.log(err);
            }
            log(key, value);
            console.log("=====================================");
        });
}

function log(key, value) {
    console.log('send message to kafka:--datetime: %s--key: %s--value: %s',
        moment().format('YYYY-MM-DD HH:mm:ss'),
        key,
        value);
}

// 消息消费者
var consumer = new HighLevelConsumer(
    client, 
    [{topic: topics.abc}], 
    {groupId: groupId.abc}
);
consumer.on('message', function (message) {
    console.log(message);
});
```

### 参考博文

1. [工作日志——k8s_pv/pvc](http://blog.csdn.net/xts_huangxin/article/details/51494472)
2. [工作日志——k8s_pv/pvc二](http://blog.csdn.net/xts_huangxin/article/details/51500358)
3. [Graceful shutdown of pods with Kubernetes](https://pracucci.com/graceful-shutdown-of-kubernetes-pods.html)
4. [Kubernetes 1.5配置Job](http://www.cnblogs.com/breezey/p/6582754.html)
5. [kafka-node](https://www.npmjs.com/package/kafka-node#install-kafka)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/11/Deploy-Kafka-And-ZP-With-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。


