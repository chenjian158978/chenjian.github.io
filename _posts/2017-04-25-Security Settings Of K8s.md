---
layout:     post
title:      "Kubernetes集群之安全设置"
subtitle:   "Security Settings Of K8s"
date:       Tue, Apr 25 2017 13:46:05 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Security-Settings-Of-K8s/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Kubernetes
---

### 系列博文

- [在CentOS7上使用二进制方式部署Kubernetes](https://o-my-chenjian.com/2017/04/25/Deploy-K8s-By-Source-Code-On-CentOS7/)
- [Kubernetes集群之安全设置](https://o-my-chenjian.com/2017/04/25/Security-Settings-Of-K8s/)
- [Kubernetes集群之搭建ETCD集群](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Kubernetes集群之创建kubeconfig文件](https://o-my-chenjian.com/2017/04/26/Create-The-File-Of-Kubeconfig-For-K8s/)
- [Kubernetes集群之Master节点](https://o-my-chenjian.com/2017/04/26/Deploy-Master-Of-K8s/)
- [Kubernetes集群之Node节点](https://o-my-chenjian.com/2017/04/26/Deploy-Node-Of-K8s/)
- [带你玩转Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Kubernetes集群之Kubedns](https://o-my-chenjian.com/2017/04/26/Deploy-Kubedns-Of-K8s/)
- [Kubernetes集群之Dashboard](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)

### K8s集群的安全设置

Kubernetes的安全设置有两种：

- 基于Certificate Authority(CA)签名的双向数字证书认证
- 基于HTTP BASE/TOKEN的认证

其中以CA证书为安全设置的安全性最高。

所有资源可以在[这里](https://pan.baidu.com/s/1pLhmqzL)进行下载

以下使用CloudFlare的PKI工具集[cfssl](https://github.com/cloudflare/cfssl)来生成CA证书


### 集群部件所需证书

|  CA&Key  |     etcd      | kube-apiserver | kube-proxy |kubelet| kubectl|
|:-----:|:------------:|:----------:|:-----:|:-----:|:-----:|
| ca.pem | ✔️ | ✔️ | ✔️ |✔️|✔️|
| ca-key.pem | | | | | |
| kubernetes.pem | ✔️ |✔️ | ✔️ | | |
| kubernetes-key.pem | ✔️| ✔️ | ✔️ | | |
| kube-proxy.pem |  | | | | |
| kube-proxy-key.pem |  | | | | |
| admin.pem |  | | | | ✔️|
| admin-key.pem|  | | | | ✔️| 


### CFSSL的安装

操作服务器IP：`192.168.1.171`，即`K8s-master`

##### 准备工作

``` bash
# 更新源
yum update -y
yum install -y vim
yum install -y wget

# 更改hostname
ipname=192-168-1-171
nodetype=master

echo "${ipname}.${nodetype}" > /etc/hostname
echo "127.0.0.1   ${ipname}.${nodetype}" >> /etc/hosts
sysctl kernel.hostname=${ipname}.${nodetype}

# 关闭防火墙
sudo systemctl stop firewalld
sudo systemctl disable firewalld
```

设置集群的环境变量

``` bash
# 创建必要的文件夹
mkdir /root/local
mkdir /root/local/bin

# 环境变量
cat >> /etc/profile <<EOF
# 最好使用 主机未用的网段 来定义服务网段和 Pod 网段

ETCD_0=192.168.1.175
ETCD_1=192.168.1.176
ETCD_2=192.168.1.177

# 服务网段 (Service CIDR），部署前路由不可达，部署后集群内使用IP:Port可达
SERVICE_CIDR="10.254.0.0/16"

# POD 网段 (Cluster CIDR），部署前路由不可达，**部署后**路由可达(flanneld保证)
CLUSTER_CIDR="172.30.0.0/16"

# 服务端口范围 (NodePort Range)，建议使用高端口
export NODE_PORT_RANGE="30000-50000"

# etcd 集群服务地址列表
export ETCD_ENDPOINTS="https://\${ETCD_0}:2379,https://\${ETCD_1}:2379,https://\${ETCD_2}:2379"

# flanneld网络配置前缀
export FLANNEL_ETCD_PREFIX="/kubernetes/network"

# kubernetes服务IP 
# 一般是SERVICE_CIDR中第一个IP
export CLUSTER_KUBERNETES_SVC_IP="10.254.0.1"

# 集群DNS服务IP 
# 从 SERVICE_CIDR 中预分配
export CLUSTER_DNS_SVC_IP="10.254.0.2"

# 集群DNS域名
export CLUSTER_DNS_DOMAIN="cluster.local."

# 将创建好的文件夹加入环境变量
# 后续的kubectl，kubelet等工具将放到该路径下
export PATH=/root/local/bin:\$PATH
EOF

# 激活配置
source /etc/profile
``` 

##### 安装CFSSL

``` bash
wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
chmod +x cfssl_linux-amd64
sudo mv cfssl_linux-amd64 /root/local/bin/cfssl

wget https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
chmod +x cfssljson_linux-amd64
sudo mv cfssljson_linux-amd64 /root/local/bin/cfssljson

wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64
chmod +x cfssl-certinfo_linux-amd64
sudo mv cfssl-certinfo_linux-amd64 /root/local/bin/cfssl-certinfo

mkdir ssl
cd ssl
cfssl print-defaults config > config.json
cfssl print-defaults csr > csr.json
```

### 创建ca.pem和ca-key.pem

##### CA配置文件

``` bash
cat >> ca-config.json <<EOF 
{
    "signing": {
        "default": {
            "expiry": "8760h"
        },
        "profiles": {
            "kubernetes": {
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth",
                    "client auth"
                ],
                "expiry": "8760h"
            }
        }
    }
}

EOF
```

- ca-config.json：可以定义多个profiles，分别指定不同的过期时间、使用场景等参数；后续在签名证书时使用某个profile

- signing：表示该证书可用于签名其它证书；生成的`ca.pem`证书中CA=TRUE

- server auth：表示client可以用该CA对server提供的证书进行验证

- client auth：表示server可以用该CA对client提供的证书进行验证

##### CA证书申请表

``` bash
cat <<EOF > ca-csr.json
{
    "CN": "kubernetes",
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "ST": "BeiJing",
            "L": "BeiJing",
            "O": "k8s",
            "OU": "System"
        }
    ]
}

EOF
```

- "CN"：Common Name，kube-apiserver从证书中提取该字段作为申请的用户名(User Name)；浏览器使用该字段验证网站是否合法

- "O"：Organization，kube-apiserver从证书中提取该字段作为申请用户所属的组 (Group)

##### 生成ca.pem/ca-key.pem

``` bash
cfssl gencert -initca ca-csr.json | cfssljson -bare ca

<<'COMMENT'
2017/04/21 14:41:50 [INFO] generating a new CA key and certificate from CSR
2017/04/21 14:41:50 [INFO] generate received request
2017/04/21 14:41:50 [INFO] received CSR
2017/04/21 14:41:50 [INFO] generating key: rsa-2048
2017/04/21 14:41:50 [INFO] encoded CSR
2017/04/21 14:41:50 [INFO] signed certificate with serial number 251797296407837937517157206505247063834323020724
COMMENT


ls ca*
<<'COMMENT'
ca-config.json  ca.csr  ca-csr.json  ca-key.pem  ca.pem
COMMENT
```

### 创建kubernetes.pem和kubernetes-key.pem

##### kubernetes证书申请表

``` bash
cat <<EOF > kubernetes-csr.json
{
  "CN": "kubernetes",
  "hosts": [
    "127.0.0.1",
    "192.168.1.171",
    "192.168.1.175",
    "192.168.1.176",
    "192.168.1.177",
    "10.254.0.1",
    "kubernetes",
    "kubernetes.default",
    "kubernetes.default.svc",
    "kubernetes.default.svc.cluster",
    "kubernetes.default.svc.cluster.local"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "BeiJing",
      "L": "BeiJing",
      "O": "k8s",
      "OU": "System"
    }
  ]
}

EOF
```

- hosts 字段分别指定了etcd集群(192.168.1.175/192.168.1.176/192.168.1.177)、k8s-master的IP(192.168.1.171)

- 添加 kube-apiserver注册的名为kubernetes的服务IP(Service Cluster IP)，一般是`kube-apiserver --service-cluster-ip-range`选项值指定的网段的第一个IP，如 "10.254.0.1"

##### 生成kubernetes.pem/kubernetes-key.pem

``` bash
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes kubernetes-csr.json | cfssljson -bare kubernetes

<<'COMMENT'
2017/04/21 14:52:32 [INFO] generate received request
2017/04/21 14:52:32 [INFO] received CSR
2017/04/21 14:52:32 [INFO] generating key: rsa-2048
2017/04/21 14:52:32 [INFO] encoded CSR
2017/04/21 14:52:32 [INFO] signed certificate with serial number 675534892777997310707325450009893653396769335719
2017/04/21 14:52:32 [WARNING] This certificate lacks a "hosts" field. This makes it unsuitable for
websites. For more information see the Baseline Requirements for the Issuance and Management
of Publicly-Trusted Certificates, v.1.1.6, from the CA/Browser Forum (https://cabforum.org);
specifically, section 10.2.3 ("Information Requirements").
COMMENT

ls kubernetes*
<<'COMMENT'
kubernetes.csr  kubernetes-csr.json  kubernetes-key.pem  kubernetes.pem
COMMENT
```

### 创建admin.pem和admin-key.pem

##### admin证书申请表

``` bash
cat <<EOF > admin-csr.json
{
  "CN": "admin",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "BeiJing",
      "L": "BeiJing",
      "O": "system:masters",
      "OU": "System"
    }
  ]
}

EOF
```

- 后续kube-apiserver使用RBAC(Role-Based Access Control)对客户端(如kubelet、kube-proxy、Pod)请求进行授权

- kube-apiserver预定义了一些RBAC使用的RoleBindings，如cluster-admin将Group system:masters与Role cluster-admin绑定，该Role授予了调用kube-apiserver所有 API的权限

- OU指定该证书的Group为`system:masters`，kubelet使用该证书访问kube-apiserver 时 ，由于证书被CA签名，所以认证通过，同时由于证书用户组为经过预授权的 `system:masters`，所以被授予访问所有API的权限

##### 生成admin.pem/admin-key.pem

``` bash
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes admin-csr.json | cfssljson -bare admin
<<'COMMENT'
2017/04/21 14:58:44 [INFO] generate received request
2017/04/21 14:58:44 [INFO] received CSR
2017/04/21 14:58:44 [INFO] generating key: rsa-2048
2017/04/21 14:58:45 [INFO] encoded CSR
2017/04/21 14:58:45 [INFO] signed certificate with serial number 592438256014219038650472041230298814450491905528
2017/04/21 14:58:45 [WARNING] This certificate lacks a "hosts" field. This makes it unsuitable for
websites. For more information see the Baseline Requirements for the Issuance and Management
of Publicly-Trusted Certificates, v.1.1.6, from the CA/Browser Forum (https://cabforum.org);
specifically, section 10.2.3 ("Information Requirements").
COMMENT

ls admin*
<<'COMMENT'
admin.csr  admin-csr.json  admin-key.pem  admin.pem
COMMENT
```

### 创建kube-proxy.pem和kube-proxy-key.pem

##### kube-proxy证书申请表

``` bash
cat <<EOF > kube-proxy-csr.json
{
  "CN": "system:kube-proxy",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "BeiJing",
      "L": "BeiJing",
      "O": "k8s",
      "OU": "System"
    }
  ]
}

EOF
```

- CN 指定该证书的User为system:kube-proxy

- kube-apiserver预定义的RoleBinding cluster-admin将User system:kube-proxy 与Role system:node-proxier绑定，该Role授予了调用kube-apiserver Proxy相关API的权限

##### 生成kube-proxy.pem/kube-proxy-key.pem

``` bash
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes  kube-proxy-csr.json | cfssljson -bare kube-proxy
<<'COMMENT'
2017/04/21 15:08:44 [INFO] generate received request
2017/04/21 15:08:44 [INFO] received CSR
2017/04/21 15:08:44 [INFO] generating key: rsa-2048
2017/04/21 15:08:45 [INFO] encoded CSR
2017/04/21 15:08:45 [INFO] signed certificate with serial number 290129049837776761536725457428661161889494017049
2017/04/21 15:08:45 [WARNING] This certificate lacks a "hosts" field. This makes it unsuitable for
websites. For more information see the Baseline Requirements for the Issuance and Management
of Publicly-Trusted Certificates, v.1.1.6, from the CA/Browser Forum (https://cabforum.org);
specifically, section 10.2.3 ("Information Requirements").
COMMENT

ls kube-proxy*
<<'COMMENT'
kube-proxy.csr  kube-proxy-csr.json  kube-proxy-key.pem  kube-proxy.pem
COMMENT
```

### 验证证书可用性

以kubernentes.pem为例

##### 利用openssl验证

``` bash
openssl x509  -noout -text -in  kubernetes.pem
<<'COMMENT'
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            76:54:08:41:9c:14:91:ce:23:59:d8:db:d5:39:66:37:67:85:e9:a7
    Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=CN, ST=BeiJing, L=BeiJing, O=k8s, OU=System, CN=kubernetes
        Validity
            Not Before: Apr 21 06:48:00 2017 GMT
            Not After : Apr 21 06:48:00 2018 GMT
        Subject: C=CN, ST=BeiJing, L=BeiJing, O=k8s, OU=System, CN=kubernetes
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (2048 bit)
                Modulus:
...
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Key Usage: critical
                Digital Signature, Key Encipherment
            X509v3 Extended Key Usage: 
                TLS Web Server Authentication, TLS Web Client Authentication
            X509v3 Basic Constraints: critical
                CA:FALSE
            X509v3 Subject Key Identifier: 
                24:FA:8A:54:54:39:D3:65:21:3F:80:E7:5C:B8:4C:F8:B9:21:B4:B0
            X509v3 Authority Key Identifier: 
                keyid:0F:64:BF:83:F1:43:0F:32:0A:E1:D8:90:7D:C6:49:7B:59:00:95:84

            X509v3 Subject Alternative Name: 
                DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster, DNS:kubernetes.default.svc.cluster.local, IP Address:127.0.0.1, IP Address:192.168.1.171, IP Address:192.168.1.175, IP Address:192.168.1.176, IP Address:192.168.1.177, IP Address:10.254.0.1
    Signature Algorithm: sha256WithRSAEncryption
...
COMMENT
```

##### 利用cfssl-certinfo验证

``` bash
cfssl-certinfo -cert kubernetes.pem
<<'COMMENT'
{
  "subject": {
    "common_name": "kubernetes",
    "country": "CN",
    "organization": "k8s",
    "organizational_unit": "System",
    "locality": "BeiJing",
    "province": "BeiJing",
    "names": [
      "CN",
      "BeiJing",
      "BeiJing",
      "k8s",
      "System",
      "kubernetes"
    ]
  },
  "issuer": {
    "common_name": "kubernetes",
    "country": "CN",
    "organization": "k8s",
    "organizational_unit": "System",
    "locality": "BeiJing",
    "province": "BeiJing",
    "names": [
      "CN",
      "BeiJing",
      "BeiJing",
      "k8s",
      "System",
      "kubernetes"
    ]
  },
  "serial_number": "675534892777997310707325450009893653396769335719",
  "sans": [
    "kubernetes",
    "kubernetes.default",
    "kubernetes.default.svc",
    "kubernetes.default.svc.cluster",
    "kubernetes.default.svc.cluster.local",
    "127.0.0.1",
    "192.168.1.171",
    "192.168.1.175",
    "192.168.1.176",
    "192.168.1.177",
    "10.254.0.1"
  ],
  "not_before": "2017-04-21T06:48:00Z",
  "not_after": "2018-04-21T06:48:00Z",
  "sigalg": "SHA256WithRSA",
...
}
COMMENT
```

### 保存证书

``` bash
sudo mkdir -p /etc/kubernetes/ssl
sudo cp *.pem /etc/kubernetes/ssl
```


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/25/Security-Settings-Of-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。


