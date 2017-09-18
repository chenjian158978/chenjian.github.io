#!/bin/bash

sudo docker run -d -e 'conf_file=redis-6379.conf' --network=host --name redis-cluster_6379 redis-cluster
sudo docker run -d -e 'conf_file=redis-6380.conf' --network=host --name redis-cluster_6380 redis-cluster
sudo docker run -d -e 'conf_file=redis-6381.conf' --network=host --name redis-cluster_6381 redis-cluster
sudo docker run -d -e 'conf_file=redis-6382.conf' --network=host --name redis-cluster_6382 redis-cluster
sudo docker run -d -e 'conf_file=redis-6383.conf' --network=host --name redis-cluster_6383 redis-cluster
sudo docker run -d -e 'conf_file=redis-6384.conf' --network=host --name redis-cluster_6384 redis-cluster
