---
layout:     post
title:      "Kubernetes集群之Kubedns"
subtitle:   "Deploy Kubedns Of K8s"
date:       Wed, Apr 26 2017 14:40:04 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Kubedns-Of-K8s/head_blog.jpg"
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


### Yaml文件

- 官方文件路径：`kubernetes/cluster/addons/dns`

- 所有的资源可以在[这里](https://pan.baidu.com/s/1pLhmqzL)进行下载

- 操作服务器IP：`192.168.1.171`，即`K8s-master`。在此之前，需要对服务器进行准备工作，具体操作请阅读Security Settings Of K8s

##### kubedns-cm.yaml

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kube-dns
  namespace: kube-system
  labels:
    addonmanager.kubernetes.io/mode: EnsureExists

```

##### kubedns-controller.yaml

``` yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: kube-dns
  namespace: kube-system
  labels:
    k8s-app: kube-dns
    kubernetes.io/cluster-service: "true"
    addonmanager.kubernetes.io/mode: Reconcile
spec:
  # replicas: not specified here:
  # 1. In order to make Addon Manager do not reconcile this replicas parameter.
  # 2. Default is 1.
  # 3. Will be tuned in real time if DNS horizontal auto-scaling is turned on.
  strategy:
    rollingUpdate:
      maxSurge: 10%
      maxUnavailable: 0
  selector:
    matchLabels:
      k8s-app: kube-dns
  template:
    metadata:
      labels:
        k8s-app: kube-dns
      annotations:
        scheduler.alpha.kubernetes.io/critical-pod: ''
    spec:
      tolerations:
      - key: "CriticalAddonsOnly"
        operator: "Exists"
      volumes:
      - name: kube-dns-config
        configMap:
          name: kube-dns
          optional: true
      containers:
      - name: kubedns
        image: gcr.io/google_containers/k8s-dns-kube-dns-amd64:1.14.1
        resources:
          # TODO: Set memory limits when we've profiled the container for large
          # clusters, then set request = limit to keep this container in
          # guaranteed class. Currently, this container falls into the
          # "burstable" category so the kubelet doesn't backoff from restarting it.
          limits:
            memory: 170Mi
          requests:
            cpu: 100m
            memory: 70Mi
        livenessProbe:
          httpGet:
            path: /healthcheck/kubedns
            port: 10054
            scheme: HTTP
          initialDelaySeconds: 60
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 5
        readinessProbe:
          httpGet:
            path: /readiness
            port: 8081
            scheme: HTTP
          # we poll on pod startup for the Kubernetes master service and
          # only setup the /readiness HTTP server once that's available.
          initialDelaySeconds: 3
          timeoutSeconds: 5
        args:
        - --domain=cluster.local.
        - --dns-port=10053
        - --config-dir=/kube-dns-config
        - --v=2
        #__PILLAR__FEDERATIONS__DOMAIN__MAP__
        env:
        - name: PROMETHEUS_PORT
          value: "10055"
        ports:
        - containerPort: 10053
          name: dns-local
          protocol: UDP
        - containerPort: 10053
          name: dns-tcp-local
          protocol: TCP
        - containerPort: 10055
          name: metrics
          protocol: TCP
        volumeMounts:
        - name: kube-dns-config
          mountPath: /kube-dns-config
      - name: dnsmasq
        image: gcr.io/google_containers/k8s-dns-dnsmasq-nanny-amd64:1.14.1
        livenessProbe:
          httpGet:
            path: /healthcheck/dnsmasq
            port: 10054
            scheme: HTTP
          initialDelaySeconds: 60
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 5
        args:
        - -v=2
        - -logtostderr
        - -configDir=/etc/k8s/dns/dnsmasq-nanny
        - -restartDnsmasq=true
        - --
        - -k
        - --cache-size=1000
        - --log-facility=-
        - --server=/cluster.local./127.0.0.1#10053
        - --server=/in-addr.arpa/127.0.0.1#10053
        - --server=/ip6.arpa/127.0.0.1#10053
        ports:
        - containerPort: 53
          name: dns
          protocol: UDP
        - containerPort: 53
          name: dns-tcp
          protocol: TCP
        # see: https://github.com/kubernetes/kubernetes/issues/29055 for details
        resources:
          requests:
            cpu: 150m
            memory: 20Mi
        volumeMounts:
        - name: kube-dns-config
          mountPath: /etc/k8s/dns/dnsmasq-nanny
      - name: sidecar
        image: gcr.io/google_containers/k8s-dns-sidecar-amd64:1.14.1
        livenessProbe:
          httpGet:
            path: /metrics
            port: 10054
            scheme: HTTP
          initialDelaySeconds: 60
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 5
        args:
        - --v=2
        - --logtostderr
        - --probe=kubedns,127.0.0.1:10053,kubernetes.default.svc.cluster.local.,5,A
        - --probe=dnsmasq,127.0.0.1:53,kubernetes.default.svc.cluster.local.,5,A
        ports:
        - containerPort: 10054
          name: metrics
          protocol: TCP
        resources:
          requests:
            memory: 20Mi
            cpu: 10m
      dnsPolicy: Default  # Don't use cluster DNS.
      serviceAccountName: kube-dns
```

##### kubedns-sa.yaml

``` yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: kube-dns
  namespace: kube-system
  labels:
    kubernetes.io/cluster-service: "true"
    addonmanager.kubernetes.io/mode: Reconcile
```

##### kubedns-svc.yaml

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: kube-dns
  namespace: kube-system
  labels:
    k8s-app: kube-dns
    kubernetes.io/cluster-service: "true"
    addonmanager.kubernetes.io/mode: Reconcile
    kubernetes.io/name: "KubeDNS"
spec:
  selector:
    k8s-app: kube-dns
  clusterIP: 10.254.0.2
  ports:
  - name: dns
    port: 53
    protocol: UDP
  - name: dns-tcp
    port: 53
    protocol: TCP

```

#### 系统预定义的RoleBinding

``` bash
kubectl get clusterrolebindings system:kube-dns -o yaml

<<'COMMENT'
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  creationTimestamp: 2017-04-24T05:14:29Z
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: system:kube-dns
  resourceVersion: "56"
  selfLink: /apis/rbac.authorization.k8s.io/v1beta1/clusterrolebindingssystem%3Akube-dns
  uid: e4cdc3ec-28ac-11e7-a8fc-005056a3abcf
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:kube-dns
subjects:
- kind: ServiceAccount
  name: kube-dns
  namespace: kube-system
COMMENT
```

- 预定义的RoleBinding system:kube-dns将`kube-system`命名空间的kube-dns ServiceAccount与system:kube-dns Role绑定，该Role具有访问kube-apiserver DNS 相关API的权限

- `kubedns-controller.yaml`中定义的Pods时使用了`kubedns-sa.yaml`文件定义的 kube-dns ServiceAccount，所以具有访问kube-apiserver DNS相关API的权限

### 创建pod和svc

``` bash
kubectl create -f kubedns/
<<'COMMENT'
configmap "kube-dns" created
deployment "kube-dns" created
serviceaccount "kube-dns" created
service "kube-dns" created
COMMENT

kubectl get pods --all-namespaces -o wide
<<'COMMENT'
NAMESPACE     NAME                        READY     STATUS    RESTARTS   AGE       IP           NODE
default       nginx-ds-3srdx              1/1       Running   0          17h       172.17.0.2   192.168.1.173
kube-system   kube-dns-3574069718-m6rmr   3/3       Running   0          1m        172.17.0.3   192.168.1.173
COMMENT
```

### 检测kubedns的可用性

``` bash
cat >> my-nginx.yaml <<EOF
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: my-nginx
spec:
  replicas: 2
  template:
    metadata:
      labels:
        run: my-nginx
    spec:
      containers:
      - name: my-nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80

EOF

kubectl create -f my-nginx.yaml
<<'COMMENT'
kubectl get pods --all-namespaces -o wide
NAMESPACE     NAME                        READY     STATUS    RESTARTS   AGE       IP           NODE
default       my-nginx-3418754612-2zb9g   1/1       Running   0          4s        172.17.0.4   192.168.1.173
default       my-nginx-3418754612-qtdhd   1/1       Running   0          4s        172.17.0.5   192.168.1.173
default       nginx-ds-3srdx              1/1       Running   0          17h       172.17.0.2   192.168.1.173
kube-system   kube-dns-3574069718-m6rmr   3/3       Running   0          5m        172.17.0.3   192.168.1.173
COMMENT

# Export该Deployment, 生成my-nginx服务
kubectl expose deploy my-nginx

kubectl get svc --all-namespaces -o wide
<<'COMMENT'
NAMESPACE     NAME         CLUSTER-IP     EXTERNAL-IP   PORT(S)         AGE       SELECTOR
default       kubernetes   10.254.0.1     <none>        443/TCP         21h       <none>
default       my-nginx     10.254.5.222   <none>        80/TCP          2s        run=my-nginx
default       nginx-ds     10.254.79.44   <nodes>       80:8966/TCP     17h       app=nginx-ds
kube-system   kube-dns     10.254.0.2     <none>        53/UDP,53/TCP   5m        k8s-app=kube-dns
COMMENT

kubectl exec -it nginx-ds-3srdx -- /bin/bash

root@nginx-ds-3srdx:/# cat /etc/resolv.conf
<<'COMMENT'
nameserver 10.254.0.2
search default.svc.cluster.local. svc.cluster.local. cluster.local. node
options ndots:5
COMMENT

root@nginx-ds-3srdx:/# ping my-nginx
<<'COMMENT'
PING my-nginx.default.svc.cluster.local (10.254.5.222): 48 data bytes
^C--- my-nginx.default.svc.cluster.local ping statistics ---
31 packets transmitted, 0 packets received, 100% packet loss
COMMENT
   
root@nginx-ds-3srdx:/# ping kubernetes
<<'COMMENT'
PING kubernetes.default.svc.cluster.local (10.254.0.1): 48 data bytes
^C--- kubernetes.default.svc.cluster.local ping statistics ---
3 packets transmitted, 0 packets received, 100% packet loss
COMMENT

root@nginx-ds-3srdx:/# ping kube-dns.kube-system
<<'COMMENT'
PING kube-dns.kube-system.svc.cluster.local (10.254.0.2): 48 data bytes
^C--- kube-dns.kube-system.svc.cluster.local ping statistics ---
3 packets transmitted, 0 packets received, 100% packet loss
COMMENT
```

Dns解析正常

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/26/Deploy-Kubedns-Of-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
