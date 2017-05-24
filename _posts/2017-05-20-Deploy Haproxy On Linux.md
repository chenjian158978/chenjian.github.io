---
layout:     post
title:      "在Linux上部署Haproxy"
subtitle:   "Deploy Haproxy On Linux"
date:       Sat, May 20 2017 09:44:00 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Haproxy-On-Linux/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Linux
---

### 下载Haproxy

部署服务器IP：192.168.1.162

``` sh
# 关闭防火墙
sudo systemctl stop firewalld
sudo systemctl disable firewalld

# yum升级
yum update -y

# 安装gcc
yum install -y gcc

# 查看TARGET值
uname -r
<<'COMMENT'
3.10.0-514.16.1.el7.x86_64
COMMENT

# 当前路径
pwd
<<'COMMENT'
/home/administrator
COMMENT

# Haproxy版本为1.7.5
wget http://www.haproxy.org/download/1.7/src/haproxy-1.7.5.tar.gz
tar -zxvf haproxy-1.7.5.tar.gz
mv haproxy-1.7.5 haproxy

# 编译安装
# ”TARGET”指定编译对应的os对应的内核版本，通过”uname -r”查询内核版本呢，README文件可查询对应关系
cd haproxy
make TARGET=linux2628 PREFIX=/usr/local/haproxy
make install PREFIX=/usr/local/haproxy

<<'COMMENT'
install -d "/usr/local/haproxy/sbin"
install haproxy  "/usr/local/haproxy/sbin"
install -d "/usr/local/haproxy/share/man"/man1
install -m 644 doc/haproxy.1 "/usr/local/haproxy/share/man"/man1
install -d "/usr/local/haproxy/doc/haproxy"
for x in configuration management architecture cookie-options lua WURFL-device-detection proxy-protocol linux-syn-cookies network-namespaces DeviceAtlas-device-detection 51Degrees-device-detection netscaler-client-ip-insertion-protocol close-options SPOE intro; do \
        install -m 644 doc/$x.txt "/usr/local/haproxy/doc/haproxy" ; \
done
COMMENT

ls /usr/local/haproxy/
<<'COMMENT'
doc  sbin  share
COMMENT
```

### haproxy.cfg

``` sh
# 存放haproxy配置文件
mkdir -p /usr/local/haproxy/conf

cat >> /usr/local/haproxy/conf/haproxy.cfg <<EOF
#---------------------------------------------------------------------
# Global settings 全局设置
#---------------------------------------------------------------------
global
	# 定义全局日志,配置在本地,通过local0输出,默认是info级别，可配置两条
	log         127.0.0.1 local0 info

	# 运行路径 
    chroot      /usr/local/haproxy

    # PID文件存放路径
    pidfile /usr/local/haproxy/log/haproxy.pid	

    # 设置每haproxy进程的最大并发连接数,其等同于命令行选项“-n”
    # “ulimit -n”自动计算的结果参照此参数设定.
    maxconn 51200

    # 后台运行haproxy
    daemon

    # 定义统计信息保存位置
    stats socket /usr/local/haproxy/stats
    
#---------------------------------------------------------------------
# Defaults settings 默认设置
#---------------------------------------------------------------------
defaults
    # 默认的模式【tcp:4层；http:7层；health:只返回OK】
	mode http

	# 继承全局的日志定义输出
	log  global

	# 日志类别
	option httplog

	# 如果后端服务器需要获得客户端真实ip需要配置的参数，可以从Http Header中获得客户端ip
	option forwardfor

	# 开启http协议中服务器端关闭功能,每个请求完毕后主动关闭http通道,使得支持长连接，使得会话可以被重用，使得每一个日志记录都会被记录.
    option httpclose

    # 如果产生了一个空连接，那这个空连接的日志将不会记录.
	option dontlognull

	# 当与后端服务器的会话失败(服务器故障或其他原因)时,把会话重新分发到其他健康的服务器上;当故障服务器恢复时,会话又被定向到已恢复的服务器上;
	option redispatch

	# 还可以用”retries”关键字来设定在判定会话失败时的尝试连接的次数
	retries 3

	# 当haproxy负载很高时,自动结束掉当前队列处理比较久的链接.
	option abortonclose

	# 默认http请求超时时间
	timeout http-request    10s

	# 默认队列超时时间,后端服务器在高负载时,会将haproxy发来的请求放进一个队列中.
    timeout queue           1m

    # haproxy与后端服务器连接超时时间.
    timeout connect         10s

    # 客户端与haproxy连接后,数据传输完毕,不再有数据传输,即非活动连接的超时时间.
    timeout client          1m

    # haproxy与后端服务器非活动连接的超时时间.
    timeout server          1m

    # 默认新的http请求连接建立的超时时间，时间较短时可以尽快释放出资源，节约资源.
    timeout http-keep-alive 10s

    # 心跳检测超时时间
    timeout check           10s

    #最大并发连接数
    maxconn                 3000


#---------------------------------------------------------------------
# listen haproxy UI 监控页面配置
#---------------------------------------------------------------------
listen admin_status
	# 配置监控运行模式
	mode http 

	# 配置统计页面访问端口
	bind 0.0.0.0:1080

	# 统计页面默认最大连接数
	maxconn 10

	# http日志格式
	option httplog

	# 开启统计
	stats enable

	# 监控页面自动刷新时间
	stats refresh 30s

	# 统计页面访问url，即访问http://ip:1080/stats
	stats uri /stats

	#监控页面的用户和密码:admin,可设置多个用户名
	stats auth admin:admin

	# 手工启动/禁用后端服务器,可通过web管理节点
	stats admin if TRUE

	# 设置haproxy错误页面
	errorfile 400 /usr/local/haproxy/errorfiles/400.http
	errorfile 403 /usr/local/haproxy/errorfiles/403.http
	errorfile 408 /usr/local/haproxy/errorfiles/408.http
	errorfile 500 /usr/local/haproxy/errorfiles/500.http
	errorfile 502 /usr/local/haproxy/errorfiles/502.http
	errorfile 503 /usr/local/haproxy/errorfiles/503.http
	errorfile 504 /usr/local/haproxy/errorfiles/504.http

#---------------------------------------------------------------------
# main frontend which proxys to the backends frontend配置
#---------------------------------------------------------------------
frontend kube-apiserver
	# 定义前端监听端口,建议采用bind *:80的形式，否则做集群高可用的时候有问题，vip切换到其余机器就不能访问.
	bind *:5002

	#如果以上规则都不匹配时，将请求转交到app组处理.
	default_backend app


#---------------------------------------------------------------------
# round robin balancing between the various backends backend配置
#---------------------------------------------------------------------
backend app
	# 根据http头进行转发,无该头部则转为使用roundrobin.
	balance roundrobin

	mode http

	# 后端服务器定义, maxconn 1024表示该服务器的最大连接数, cookie 1表示serverid为1,weight代表权重(默认1，最大为265，0则表示不参与负载均衡),
	#check inter 1500是检测心跳频率, rise 2是2次正确认为服务器可用, fall 3是3次失败认为服务器不可用.
	server app1 192.168.1.153:8080 maxconn 1024 cookie 1 weight 3 check inter 1500 rise 2 
	server app2 192.168.1.154:8080 maxconn 1024 cookie 1 weight 3 check inter 1500 rise 2 
	server app3 192.168.1.155:8080 maxconn 1024 cookie 1 weight 3 check inter 1500 rise 2

EOF

```

### 所需文件

``` sh
# errorfile错误文件
cp -R haproxy/examples/errorfiles/ /usr/local/haproxy/

# haproxy日志文件
mkdir -p /usr/local/haproxy/log
touch /usr/local/haproxy/log/haproxy.log
ln -s /usr/local/haproxy/log/haproxy.log /var/log/

# etc中的haproxy文件
mkdir -p /etc/haproxy
ln -s /usr/local/haproxy/conf/haproxy.cfg /etc/haproxy/

# 配置开机自动启动
cp haproxy/examples/haproxy.init /etc/rc.d/init.d/haproxy
chmod +x /etc/rc.d/init.d/haproxy
chkconfig --add haproxy
chkconfig haproxy on

# 设置全局启动文件
ln -s /usr/local/haproxy/sbin/haproxy /usr/sbin/
```

### 配置rsyslog

haproxy默认没有日志，依靠rsyslog收集日志

``` sh
# 注意loacl0需要与haproxy.cfg文件中对应
echo -e '$ModLoad imudp \n $UDPServerRun 514 \n local0.* /var/log/haproxy.log' >> /etc/rsyslog.conf

# 重启rsyslog服务
systemctl restart rsyslog
```

### 关闭selinux

``` sh
setenforce 0
```

### 配置防火墙

``` sh
# 安装iptables-services
sudo yum install -y iptables-services

systemctl status iptables
<<'COMMENT'
● iptables.service - IPv4 firewall with iptables
   Loaded: loaded (/usr/lib/systemd/system/iptables.service; disabled; vendor preset: disabled)
   Active: inactive (dead)
COMMENT

# 可以看出有个辅助文件路径/etc/sysconfig/iptables
cat /usr/lib/systemd/system/iptables.service
<<'COMMENT'
[Unit]
Description=IPv4 firewall with iptables
After=syslog.target
AssertPathExists=/etc/sysconfig/iptables

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/libexec/iptables/iptables.init start
ExecReload=/usr/libexec/iptables/iptables.init reload
ExecStop=/usr/libexec/iptables/iptables.init stop
Environment=BOOTUP=serial
Environment=CONSOLETYPE=serial
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=basic.target
COMMENT

# 写入iptables配置，注意涉及所需端口
sed -i '/REJECT/d' /etc/sysconfig/iptables
sed -i '/COMMIT/i \-A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT' /etc/sysconfig/iptables
sed -i '/COMMIT/i \-A INPUT -p tcp -m state --state NEW -m tcp --dport 1080 -j ACCEPT' /etc/sysconfig/iptables
sed -i '/COMMIT/i \-A INPUT -p tcp -m state --state NEW -m tcp --dport 5002 -j ACCEPT' /etc/sysconfig/iptables

# 开启服务
systemctl restart iptables.service

iptables -L -v -n --line-number
<<'COMMENT'
Chain INPUT (policy ACCEPT 87 packets, 8556 bytes)
num   pkts bytes target     prot opt in     out     source               destination         
1        0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:80
2        0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:1080
3        0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:5002

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 52 packets, 10640 bytes)
num   pkts bytes target     prot opt in     out     source               destination
COMMENT
```

### 启动Haproxy

``` sh
systemctl start haproxy

systemctl status haproxy
<<'COMMENT'
● haproxy.service - SYSV: HA-Proxy is a TCP/HTTP reverse proxy which is particularly suited for high availability environments.
   Loaded: loaded (/etc/rc.d/init.d/haproxy; bad; vendor preset: disabled)
   Active: active (running) since Sat 2017-05-20 13:36:13 CST; 1s ago
     Docs: man:systemd-sysv-generator(8)
  Process: 21196 ExecStart=/etc/rc.d/init.d/haproxy start (code=exited, status=0/SUCCESS)
 Main PID: 21201 (haproxy)
   CGroup: /system.slice/haproxy.service
           └─21201 /usr/sbin/haproxy -D -f /etc/haproxy/haproxy.cfg -p /var/run/haproxy.pid

May 20 13:36:13 192-168-1-162.node-2 systemd[1]: Starting SYSV: HA-Proxy is a TCP/HTTP reverse proxy which is particularly suited for high availab...ents....
May 20 13:36:13 192-168-1-162.node-2 haproxy[21196]: /etc/rc.d/init.d/haproxy: line 26: [: =: unary operator expected
May 20 13:36:13 192-168-1-162.node-2 haproxy[21196]: Starting haproxy: [  OK  ]
May 20 13:36:13 192-168-1-162.node-2 systemd[1]: Started SYSV: HA-Proxy is a TCP/HTTP reverse proxy which is particularly suited for high availabi...nments..
Hint: Some lines were ellipsized, use -l to show in full.
COMMENT


netstat -ntlp
<<'COMMENT'
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      942/sshd            
tcp        0      0 0.0.0.0:1080            0.0.0.0:*               LISTEN      21201/haproxy       
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      1760/master         
tcp        0      0 0.0.0.0:5002            0.0.0.0:*               LISTEN      21201/haproxy       
tcp6       0      0 :::22                   :::*                    LISTEN      942/sshd            
tcp6       0      0 ::1:25                  :::*                    LISTEN      1760/master  
COMMENT
```

### 访问Haproxy控制台

地址：http://192.168.1.162:1080/stats
输入账户admin密码admin

![Haproxy控制台](/img/in-post/Deploy-Haproxy-On-Linux/haproxy.jpg)





<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/05/20/Deploy-Haproxy-On-Linux/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。


