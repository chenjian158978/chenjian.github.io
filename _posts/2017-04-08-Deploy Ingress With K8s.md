---
layout:     post
title:      "Deploy Ingress With K8s"
subtitle:   "I may tell all my bones:
they look and stare upon me. Psa 22:17"
date:       Sat, Apr 8 2017 09:47:17 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Ingress-With-K8s/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Kubernetes
---

### 系列博文

- [Deploy K8s by Kubeadm on Linux](https://o-my-chenjian.com/2016/12/08/Deploy-K8s-by-Kubeadm-on-Linux/)
- [Easy With Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Deploy Etcd Cluster](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Deploy Dashboard With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)
- [Deploy Monitoring With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Monitoring-With-K8s/)
- [Deploy Logging With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/)
- [Deploy Ingress With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Ingress-With-K8s/)
- [Deploy Redis Sentinel Cluster With K8s](https://o-my-chenjian.com/2017/02/06/Deploy-Redis-Sentinel-Cluster-With-K8s/)
- [Deploy Kafka And ZP With K8s](https://o-my-chenjian.com/2017/04/11/Deploy-Kafka-And-ZP-With-K8s/)

### 下载yaml文件

读者想要对应的yaml文件，可到[这里](https://pan.baidu.com/s/1pLhmqzL)进行下载。

### 部署默认后端

`kubectl create -f default-backend.yaml`

### 部署 Ingress Controller

修改yaml文件中，添加`hostNetwork: true`，使其监听宿主机 80 端口：

``` sh
spec:
  template:
    metadata:
      labels:
        name: nginx-ingress-lb
    spec:
      terminationGracePeriodSeconds: 60
      hostNetwork: true
```

`kubectl create -f nginx-ingress-daemonset.yaml`

### 部署 Ingress

`kubectl create -f dashboard-ingress.yaml`

### 修改hosts文件

添加集群中的某个node或master的IP到hosts文件中，例如Linux系统：

`echo "10.0.0.171  dashboard.chenjian.com" >> /etc/hosts`

### Ingress部署TLS（HTTPS）

##### 创建证书

``` bash
# 生成CA自签证书文件夹
mkdir cert && cd cert

# 生成CA自签证书的密钥
openssl genrsa -out ca-key.pem 2048

# 生成CA自签证书
openssl req -x509 -new -nodes -key ca-key.pem -days 10000 -out ca.pem -subj "/CN=kube-ca"

# 配置openssl部署
cp /etc/pki/tls/openssl.cnf .
vim openssl.cnf

# 修改如下
[ req ]
req_extensions = v3_req # 这行默认注释关着的 把注释删掉
# 下面配置是新增的
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = dashboard.chenjian.me
DNS.2 = kibana.chenjian.me

# 生成证书密钥
openssl genrsa -out ingress-key.pem 2048

# 生成证书的申请表
openssl req -new -key ingress-key.pem -out ingress.csr -subj "/CN=kube-ingress" -config openssl.cnf

# 生成证书 有效期为365天
openssl x509 -req -in ingress.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out ingress.pem -days 365 -extensions v3_req -extfile openssl.cnf
```

##### 创建secret

ingress-secret.yaml文件格式如下：

``` sh
apiVersion: v1
data:
  tls.crt: ##内容为ingress.pem里的内容##
  tls.key: ##内容为ingress-key.pem里的内容##
kind: Secret
metadata:
  name: ingress-secret
  namespace: kube-system
type: Opaque
```

create完成：

`kubectl create -f ingress-secret.yaml`

或者直接用文件：

`kubectl create secret tls ingress-secret --key cert/ingress-key.pem --cert cert/ingress.pem --namespace kube-system`

##### 部署Ingress

`kubectl create -f dashboard-ingress-tls.yaml`

##### 修改hosts文件

添加集群中的某个node或master的IP到hosts文件中，例如Linux系统：

`echo "10.0.0.171  dashboard.chenjian.com" >> /etc/hosts`

##### 访问地址dashboard.chenjian.com

部署TLS后的80端口会自动重定向到443（HTTPS端口）

开始出现“Your connnection is not private”

在chrome浏览器中，HTTPS/SSL中添加ca.pem文件，并给予全部权限。

再次打开，没有https提示（钥匙上带叉的logo），但是URL栏中出现“Not Secure”这样的红色字样。

解决这个问题，需要重服务商买权威的CA证书。

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/08/Deploy-Ingress-With-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。