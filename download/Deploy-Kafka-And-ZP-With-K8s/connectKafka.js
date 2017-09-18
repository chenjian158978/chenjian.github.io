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
