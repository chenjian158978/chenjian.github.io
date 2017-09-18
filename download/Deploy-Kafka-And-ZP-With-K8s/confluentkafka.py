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
    # TestConfluentKafka().test_producer()
    TestConfluentKafka().test_consumer()
