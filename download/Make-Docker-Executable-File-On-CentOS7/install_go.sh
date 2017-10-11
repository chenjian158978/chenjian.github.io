#!/bin/bash

cur_path=`pwd`

# 解压go包
sudo tar zxvf ${cur_path}/go1.8.4.linux-amd64.tar.gz -C /usr/local

# 创建GOPATH文件夹
sudo mkdir -p /home/mygo

# 设置go环境变量
sudo echo "export GOROOT=/usr/local/go" >> /etc/profile
sudo echo "export GOPATH=/home/mygo" >> /etc/profile
sudo echo "export PATH=\$PATH:\$GOROOT/bin" >> /etc/profile
. /etc/profile

# 安装wget
sudo yum install -y wget

# 更新为aliyun源
sudo wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

# 安装git
sudo yum install -y git

# 安装go包管理工具govendor
go get -u github.com/kardianos/govendor
cp ${GOPATH}/bin/govendor /usr/local/go/bin/
