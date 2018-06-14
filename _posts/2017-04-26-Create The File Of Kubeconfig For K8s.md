---
layout:     post
title:      "Kubernetes集群之创建kubeconfig文件"
subtitle:   "Create The File Of Kubeconfig For K8s"
date:       Wed, Apr 26 2017 09:21:03 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Create-The-File-Of-Kubeconfig-For-K8s/head_blog.jpg"
catalog:    true
tags: [工作, Kubernetes]
---

### 系列博文

- [在CentOS7上使用二进制方式部署Kubernetes](https://o-my-chenjian.com/2017/04/25/Deploy-K8s-By-Source-Code-On-CentOS7/)
- [Kubernetes集群之安全设置](https://o-my-chenjian.com/2017/04/25/Security-Settings-Of-K8s/)
- [Kubernetes集群之搭建ETCD集群](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Kubernetes集群之创建kubeconfig文件](https://o-my-chenjian.com/2017/04/26/Create-The-File-Of-Kubeconfig-For-K8s/)
- [Kubernetes集群之Flannel网络](https://o-my-chenjian.com/2017/05/11/Deploy-Pod-Network-Of-Flannel/)
- [Kubernetes集群之Master节点](https://o-my-chenjian.com/2017/04/26/Deploy-Master-Of-K8s/)
- [Kubernetes集群之高可用性Master集群](https://o-my-chenjian.com/2017/05/20/Deploy-HA-Master-Clusters-Of-K8s/)
- [Kubernetes集群之Node节点](https://o-my-chenjian.com/2017/04/26/Deploy-Node-Of-K8s/)
- [带你玩转Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Kubernetes集群之Kubedns](https://o-my-chenjian.com/2017/04/26/Deploy-Kubedns-Of-K8s/)
- [Kubernetes集群之Dashboard](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)
- [Kubernetes集群之Monitoring](https://o-my-chenjian.com/2017/04/08/Deploy-Monitoring-With-K8s/)
- [Kubernetes集群之Logging](https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/)
- [Kubernetes集群之清除集群](https://o-my-chenjian.com/2017/05/11/Clear-The-Cluster-Of-K8s/)


### Kubeconfig文件

kubeconfig文件记录k8s集群的各种信息，对集群构建非常重要。

- kubectl命令行工具从`~/.kube/config`，即kubectl的kubeconfig文件中获取访问`kube-apiserver`的地址，证书和用户名等信息

- kubelet/kube-proxy等在Node上的程序进程同样通过`bootstrap.kubeconfig`和`kube-proxy.kubeconfig`上提供的认证与授权信息与Master进行通讯


### 下载kubectl二进制文件

##### 增加环境变量

操作服务器IP：`192.168.1.171`，即`K8s-master`。在此之前，需要对服务器进行**准备工作，例如环境变量的设置**，具体操作请阅读[Kubernetes集群之安全设置](https://o-my-chenjian.com/2017/04/25/Security-Settings-Of-K8s/)

- KUBE_APISERVER指定kubectl访问的`kube-apiserver`的地址，后续被写入`~/.kube/config`配置文件

- BOOTSTRAP_TOKEN将被写入到kube-apiserver使用的`token.csv`文件和kubelet使用的`bootstrap.kubeconfig`文件，如果后续重新生成了BOOTSTRAP_TOKEN，则需要：

	- 更新token.csv文件，分发到所有机器(master和node的`/etc/kubernetes/`目录下
	- 重新生成`bootstrap.kubeconfig`文件，分发到所有node机器的`/etc/kubernetes/`目录下
	- 重启kube-apiserver和kubelet进程
	- 重新approve kubelet的csr请求

##### 下载二进制文件

``` bash
wget https://dl.k8s.io/v1.6.2/kubernetes-client-linux-amd64.tar.gz
tar -xzvf kubernetes-client-linux-amd64.tar.gz
sudo cp kubernetes/client/bin/kube* /root/local/bin/
chmod a+x /root/local/bin/kube*
```

所有的资源可以在[这里](https://pan.baidu.com/s/1pLhmqzL)进行下载

### 生成Token文件

Kubelet在首次启动时，会向kube-apiserver发送`TLS Bootstrapping`请求。如果kube-apiserver验证其与自己的token.csv一致，则为kubelete生成CA与key。

``` bash
# 生成Token文件
cat > token.csv <<EOF 
${BOOTSTRAP_TOKEN},kubelet-bootstrap,10001,"system:kubelet-bootstrap"
EOF

cp token.csv /etc/kubernetes/
```

### 生成kubectl的kubeconfig文件

``` bash
# 设置集群参数
kubectl config set-cluster kubernetes \
--certificate-authority=/etc/kubernetes/ssl/ca.pem \
--embed-certs=true \
--server=${KUBE_APISERVER}

<<'COMMENT'
Cluster "kubernetes" set.
COMMENT

# 设置客户端认证参数
kubectl config set-credentials admin \
--client-certificate=/etc/kubernetes/ssl/admin.pem \
--embed-certs=true \
--client-key=/etc/kubernetes/ssl/admin-key.pem

<<'COMMENT'
User "admin" set.
COMMENT

# 设置上下文参数
kubectl config set-context kubernetes \
--cluster=kubernetes \
--user=admin

<<'COMMENT'
Context "kubernetes" set.
COMMENT

# 设置默认上下文
kubectl config use-context kubernetes

<<'COMMENT'
Switched to context "kubernetes".
COMMENT
```

- admin.pem证书的OU字段值为`system:masters`，kube-apiserver预定义的RoleBinding cluster-admin 将 Group system:masters 与 Role cluster-admin 绑定，该Role授予了调用kube-apiserver相关API的权限

- 生成的kubeconfig被保存到`~/.kube/config`文件

``` sh
ls ~/.kube/
<<'COMMENT'
config
COMMENT
```


### 生成kubelet的bootstrapping kubeconfig文件

``` bash
kubectl config set-cluster kubernetes \
--certificate-authority=/etc/kubernetes/ssl/ca.pem \
--embed-certs=true \
--server=${KUBE_APISERVER} \
--kubeconfig=bootstrap.kubeconfig

<<'COMMENT'
Cluster "kubernetes" set.
COMMENT

# 设置客户端认证参数
kubectl config set-credentials kubelet-bootstrap \
--token=${BOOTSTRAP_TOKEN} \
--kubeconfig=bootstrap.kubeconfig

<<'COMMENT'
User "kubelet-bootstrap" set.
COMMENT

# 设置上下文参数
kubectl config set-context default \
--cluster=kubernetes \
--user=kubelet-bootstrap \
--kubeconfig=bootstrap.kubeconfig

<<'COMMENT'
Context "default" set.
COMMENT


# 设置默认上下文
kubectl config use-context default --kubeconfig=bootstrap.kubeconfig

<<'COMMENT'
Switched to context "default".
COMMENT
```

- `--embed-certs`为true时表示将certificate-authority证书写入到生成的`bootstrap.kubeconfig`文件中
- 设置kubelet客户端认证参数时没有指定秘钥和证书，后续由kube-apiserver自动生成；
- 生成的`bootstrap.kubeconfig`文件会在当前文件路径下

### 生成kube-proxy的kubeconfig文件

``` bash
# 设置集群参数
kubectl config set-cluster kubernetes \
--certificate-authority=/etc/kubernetes/ssl/ca.pem \
--embed-certs=true \
--server=${KUBE_APISERVER} \
--kubeconfig=kube-proxy.kubeconfig

<<'COMMENT'
Cluster "kubernetes" set.
COMMENT

# 设置客户端认证参数
kubectl config set-credentials kube-proxy \
--client-certificate=/etc/kubernetes/ssl/kube-proxy.pem \
--client-key=/etc/kubernetes/ssl/kube-proxy-key.pem \
--embed-certs=true \
--kubeconfig=kube-proxy.kubeconfig

<<'COMMENT'
User "kube-proxy" set.
COMMENT

# 设置上下文参数
kubectl config set-context default \
--cluster=kubernetes \
--user=kube-proxy \
--kubeconfig=kube-proxy.kubeconfig

<<'COMMENT'
Context "default" set.
COMMENT

# 设置默认上下文
kubectl config use-context default --kubeconfig=kube-proxy.kubeconfig

<<'COMMENT'
Switched to context "default".
COMMENT
```

- `--embed-cert` 都为 true，这会将`certificate-authority`、`client-certificate`和`client-key`指向的证书文件内容写入到生成的`kube-proxy.kubeconfig`文件中

- kube-proxy.pem证书中CN为`system:kube-proxy`，kube-apiserver预定义的 RoleBinding cluster-admin将User system:kube-proxy与Role system:node-proxier绑定，该Role授予了调用kube-apiserver Proxy相关API的权限

### 将kubeconfig文件拷贝至Node上

操作服务器IP：

- `192.168.1.171`，即`K8s-master`
- `192.168.1.173`和`192.168.1.174`，即两台`K8s-node`

将生成的两个kubeconfig文件拷贝到所有的Node的`/etc/kubernetes/`

``` bash
sudo cp bootstrap.kubeconfig kube-proxy.kubeconfig /etc/kubernetes/
```


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/26/Create-The-File-Of-Kubeconfig-For-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。


