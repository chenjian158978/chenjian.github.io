---
layout:     post
title:      "CentOS7遇上FTP"
subtitle:   "Deploy FTP On CentOS7"
date:       Fri, Aug 11 2017 14:16:46 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-FTP-On-CentOS7/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Python
---

### 安装配置vsftp

##### 防火墙与21端口

- 关闭firewall

``` sh
systemctl stop firewalld.service
systemctl disable firewalld.service
```

- 换用iptables

[在Centos7上使用Iptables](https://o-my-chenjian.com/2017/02/28/Using-Iptables-On-Centos7/)

- 开启21端口

``` sh
sudo vim /etc/sysconfig/iptables

<<'COMMENT'
# you can edit this manually or use system-config-firewall
# please do not ask us to add additional ports/services to this default configuration
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 21 -j ACCEPT
-A INPUT -j REJECT --reject-with icmp-host-prohibited
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
COMMIT
COMMENT

systemctl restart iptables.service
systemctl enable iptables.service
```

- 关闭SELINUX

``` sh
sed -i "s/SELINUX=enforcing/#SELINUX=enforcing/g" /etc/selinux/config
sed -i "s/SELINUXTYPE=targeted/#SELINUXTYPE=targeted/g" /etc/selinux/config
echo "SELINUX=disabled" >> /etc/selinux/config

setenforce 0
```

##### 安装vsftp

``` sh
yum install -y vsftpd

systemctl start vsftpd.service
systemctl enable vsftpd.service

vsftpd -v
<<'COMMENT'
vsftpd: version 3.0.2
COMMENT

netstat -ntlp
<<'COMMENT'
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1026/sshd           
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      2013/master         
tcp6       0      0 :::21                   :::*                    LISTEN      6830/vsftpd         
tcp6       0      0 :::22                   :::*                    LISTEN      1026/sshd           
COMMENT
```

##### 配置vsftp

``` sh
cp /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf-bak

sed -i "s/anonymous_enable=YES/anonymous_enable=NO/g" /etc/vsftpd/vsftpd.conf

sed -i "s/#anon_upload_enable=YES/anon_upload_enable=NO/g" /etc/vsftpd/vsftpd.conf

sed -i "s/#anon_mkdir_write_enable=YES/anon_mkdir_write_enable=YES/g" /etc/vsftpd/vsftpd.conf

sed -i "s/#chown_uploads=YES/chown_uploads=NO/g" /etc/vsftpd/vsftpd.conf

sed -i "s/#async_abor_enable=YES/async_abor_enable=YES/g" /etc/vsftpd/vsftpd.conf

sed -i "s/#ascii_upload_enable=YES/ascii_upload_enable=YES/g" /etc/vsftpd/vsftpd.conf

sed -i "s/#ascii_download_enable=YES/ascii_download_enable=YES/g" /etc/vsftpd/vsftpd.conf

sed -i "s/#ftpd_banner=Welcome to blah FTP service./ftpd_banner=Welcome to FTP service./g" /etc/vsftpd/vsftpd.conf

cat >> /etc/vsftpd/vsftpd.conf <<EOF 
use_localtime=YES
listen_port=21
chroot_local_user=YES
idle_session_timeout=300
guest_enable=YES
guest_username=vsftpd
user_config_dir=/etc/vsftpd/vconf
data_connection_timeout=1
virtual_use_local_privs=YES
pasv_min_port=10060
pasv_max_port=10090
accept_timeout=5
connect_timeout=1
dual_log_enable=YES 
vsftpd_log_file=/var/log/vsftpd.log 
EOF
```

##### 建立虚拟用户

第一行行号，第二行密码，第三行账号，第四行密码，以此类推，不能使用`root`，系统保留。

``` sh
cat >> /etc/vsftpd/virtusers <<EOF
chenjian
chenjian
EOF
```

##### 生成用户数据文件

``` sh
db_load -T -t hash -f /etc/vsftpd/virtusers /etc/vsftpd/virtusers.db

chmod 600 /etc/vsftpd/virtusers.db 
```

##### 修改PAM文件

``` sh
cp /etc/pam.d/vsftpd /etc/pam.d/vsftpd.bak

sed -i 's/^auth\|^account/#&/g' /etc/pam.d/vsftpd

cat >> /etc/pam.d/vsftpd <<EOF
auth sufficient /lib64/security/pam_userdb.so db=/etc/vsftpd/virtusers
account sufficient /lib64/security/pam_userdb.so db=/etc/vsftpd/virtusers
EOF
```

##### 新建用户vsftp

用户登录终端设为/bin/false(即：使之不能登录系统)

``` sh
useradd vsftpd -d /home/vsftpd -s /bin/false
chown -R vsftpd:vsftpd /home/vsftpd
```

##### 建立虚拟用户配置文件

``` sh
mkdir /etc/vsftpd/vconf
cd /etc/vsftpd/vconf

mkdir -p /home/vsftpd/chenjian/

cat >> /etc/vsftpd/vconf/chenjian <<EOF
local_root=/home/vsftpd/chenjian/
write_enable=YES
anon_world_readable_only=NO
anon_upload_enable=YES
anon_mkdir_write_enable=YES
anon_other_write_enable=YES
allow_writeable_chroot=YES
EOF

sudo chmod -R 777 /home/vsftpd/
```

##### 重启vsftp服务

``` sh
systemctl restart vsftpd.service
```

**自此，FTP服务器建立好**

### 使用软件Transmit连接

![ftp_transmit](/img/in-post/Deploy-FTP-On-CentOS7/ftp_transmit.jpg)

![ftp_transmit_1](/img/in-post/Deploy-FTP-On-CentOS7/ftp_transmit_1.jpg)

其中路径`\`即为`/home/vsftpd/chenjian`。

### 使用Python操作FTP

代码下载：[connectFTP.py](/download/Deploy-FTP-On-CentOS7/connectFTP.py)

``` python
# -*- coding:utf8 -*-

"""
@author: chenjian158978@gmail.com

@date: Thu, Aug 10 2017

@time: 10:05:18 GMT+8
"""
from ftplib import FTP


def ftpconnect(host, username, password, port=21):
    """ ftp链接

    :param host: ftp HOST
    :param username: ftp 用户名
    :param password: ftp 密码
    :param port: ftp 端口
    :return: ftp实例
    """
    try:
        ftp_obj = FTP()
        ftp_obj.set_debuglevel(2)
        ftp_obj.connect(host, port)
        ftp_obj.login(username, password)

        # 打印欢迎语
        print 'getwelcome:', ftp_obj.getwelcome()

        # 进入目录'/1111/'
        # ftp_obj.cwd('/1111/')

        # 打印当前目录内的文件
        for i, file_name in enumerate(ftp_obj.nlst()):
            print 'file_name_%s' % str(i), file_name

        # 打印当前的路径
        print 'current_path:', ftp_obj.pwd()

        # 新建远程目录
        ftp_obj.mkd('/new_mkdir_file')

        # 删除远程目录
        ftp_obj.rmd('/new_mkdir_file')

        # 删除远程文件
        # ftp_obj.delete('/dddd.txt')

        return ftp_obj
    except Exception as e:
        print str(e)


def downloadfile(ftp_obj, remotepath, localpath):
    """ 下载文件

    :param ftp_obj: ftp实例
    :param remotepath: 远程路径
    :param localpath: 本地路径
    :return:
    """
    try:
        # 设置的缓冲区大小
        bufsize = 1024
        fp = open(localpath, 'wb')
        ftp_obj.retrbinary('RETR ' + remotepath, fp.write, bufsize)
        ftp_obj.set_debuglevel(0)
    except Exception as e:
        print str(e)
    finally:
        fp.close()


def uploadfile(ftp_obj, remotepath, localpath):
    """ 上传文件

    :param ftp_obj: ftp实例
    :param remotepath: 远程路径
    :param localpath: 本地路径
    :return:
    """
    try:
        bufsize = 1024
        fp = open(localpath, 'rb')
        ftp_obj.storbinary('STOR ' + remotepath, fp, bufsize)
        ftp_obj.set_debuglevel(0)
    except Exception as e:
        print str(e)
    finally:
        fp.close()

if __name__ == '__main__':
    ftp = ftpconnect(host="192.168.1.179", username="chenjian", password="chenjian")
    downloadfile(ftp_obj=ftp, remotepath='dddd.jpg', localpath='/Users/jianchan/Documents/dddd1.jpg')
    uploadfile(ftp_obj=ftp, remotepath='/eeee1.jpg', localpath='/Users/jianchan/Documents/eeee.jpg')

    # FTP.quit():发送QUIT命令给服务器并关闭掉连接。
    # 这是一个比较“缓和”的关闭连接方式，但是如果服务器对QUIT命令返回错误时，会抛出异常
    # FTP.close()：单方面的关闭掉连接，不应该用在已经关闭的连接之后，例如不应用在FTP.quit()之后。
    ftp.quit()

```

运行：

``` sh
python connectFTP.py

<<'COMMENT'
*get* '220 Welcome to FTP service.\r\n'
*resp* '220 Welcome to FTP service.'
*cmd* 'USER chenjian'
*put* 'USER chenjian\r\n'
*get* '331 Please specify the password.\r\n'
*resp* '331 Please specify the password.'
*cmd* 'PASS ********'
*put* 'PASS ********\r\n'
*get* '230 Login successful.\r\n'
*resp* '230 Login successful.'
getwelcome: *welcome* '220 Welcome to FTP service.'
220 Welcome to FTP service.
*cmd* 'TYPE A'
*put* 'TYPE A\r\n'
*get* '200 Switching to ASCII mode.\r\n'
*resp* '200 Switching to ASCII mode.'
*cmd* 'PASV'
*put* 'PASV\r\n'
*get* '227 Entering Passive Mode (192,168,1,179,39,80).\r\n'
*resp* '227 Entering Passive Mode (192,168,1,179,39,80).'
*cmd* 'NLST'
*put* 'NLST\r\n'
*get* '150 Here comes the directory listing.\r\n'
*resp* '150 Here comes the directory listing.'
*get* '226 Directory send OK.\r\n'
*resp* '226 Directory send OK.'
file_name_0 dddd.jpg
file_name_1 eeee1.jpg
current_path: *cmd* 'PWD'
*put* 'PWD\r\n'
*get* '257 "/"\r\n'
*resp* '257 "/"'
/
*cmd* 'MKD /new_mkdir_file'
*put* 'MKD /new_mkdir_file\r\n'
*get* '257 "/new_mkdir_file" created\r\n'
*resp* '257 "/new_mkdir_file" created'
*cmd* 'RMD /new_mkdir_file'
*put* 'RMD /new_mkdir_file\r\n'
*get* '250 Remove directory operation successful.\r\n'
*resp* '250 Remove directory operation successful.'
*cmd* 'TYPE I'
*put* 'TYPE I\r\n'
*get* '200 Switching to Binary mode.\r\n'
*resp* '200 Switching to Binary mode.'
*cmd* 'PASV'
*put* 'PASV\r\n'
*get* '227 Entering Passive Mode (192,168,1,179,39,82).\r\n'
*resp* '227 Entering Passive Mode (192,168,1,179,39,82).'
*cmd* 'RETR dddd.jpg'
*put* 'RETR dddd.jpg\r\n'
*get* '150 Opening BINARY mode data connection for dddd.jpg (11126 bytes).\r\n'
*resp* '150 Opening BINARY mode data connection for dddd.jpg (11126 bytes).'
*get* '226 Transfer complete.\r\n'
*resp* '226 Transfer complete.'
COMMENT
```

### Shell操作FTP

代码下载：[connectFTP.sh](/download/Deploy-FTP-On-CentOS7/connectFTP.sh)

``` sh
#!/usr/bin/env bash

HOST=192.168.1.145
USER=chenjian
PASSWORD=chenjian
FILENAME=$1
LOCAL_PATH=/var/dfdfdf/
REMOTE_PATH=/home/dddd/
lftp -u ${USER},${PASSWORD} sftp://${HOST} << EOF
  lcd ${LOCAL_PATH}
  cd ${REMOTE_PATH}
  # 上传文件
  put ${FILENAME}
  
  # 下载文件
  get ${FILENAME}
  bye
EOF
```


### 参考

1. [CentOS7安装和配置FTP](http://blog.csdn.net/the_victory/article/details/52192085)
2. [两种方式建立Vsftpd虚拟用户](http://yuanbin.blog.51cto.com/363003/129071/)
3. [CentOS7 添加FTP用户并设置权限](http://blog.csdn.net/mayday920723/article/details/53173263)
4. [vsftpd日志配置及查看](https://www.zybuluo.com/zhutoulwz/note/35795)
5. [error_perm: 550 Permission denied](https://stackoverflow.com/questions/23691364/error-perm-550-permission-denied)
6. [python调用ftp.cwd('xx/xx') 产生错误：550 Failed to change directoryd的解决方法](http://blog.csdn.net/xiemanr/article/details/53326089)
7. [vsftpd悲催的“550 Failed to change directory”错误](http://heipark.iteye.com/blog/1671578)
8. [使用python操作FTP上传和下载](http://www.cnblogs.com/hltswd/p/6228992.html)
9. [python ftp的一个脚本](http://blog.csdn.net/xx5595480/article/details/53769693)
10. [详解CentOS7安装配置vsftp搭建FTP](http://www.jb51.net/article/103904.htm)
11. [python下操作ftp上传](http://www.cnblogs.com/tony-d/p/6095675.html)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/08/11/Deploy-FTP-On-CentOS7/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。









