---
layout:     post
title:      "VMware之性能优化中的就绪时间"
subtitle:   "Ready Time Of Performance Optimization In VMware"
date:       Wed, Mar 21 2018 23:04:44 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Ready-Time-Of-Performance-Optimization-In-VMware/head_blog.jpg"
catalog:    true
tags: [工作, VMware]
---


### 就绪时间

`就绪时间(Ready Time)`就是虚拟机在获取到CPU资源之前，处于`就绪状态(Ready-To-Run State)`所需的总等待时间。它是在`VMWare环境`中，分析虚拟机性能的重要CPU参数。

在[ESX3 Ready Time](https://www.vmware.com/pdf/esx3_ready_time.pdf)中写到

> 运行着Guest操作系统(Guest Operating System)的虚拟机由多部分组成，其中就包括Guest操作系统所需要的虚拟CPU(virtual CPU)，虚拟机监控(Virtual Machine Monitor)管理着虚拟机对各个资源的使用，例如CPU，内存，磁盘，网络适配器，鼠标或者键盘。本文中所涉及的调度虚拟机上的虚拟CPU到寄主机上的物理CPU。在ESX服务器上同样运行着部分进程来维持虚拟活动，这些虚拟组件与这些进程比正常的操作系统更为复杂，而在ESX服务器上的物理CPU被这所有的进程与虚拟机共同分享。

> 既然资源是被分享，则有种可能，由于资源太忙而导致被分享的资源没有被立即使用。当多个进程同时在使用同一个CPU资源，而资源未被立即使用，进程在ESX服务器将CPU分配给它之前必须要等待。ESX服务器的调度器控制在寄主机上的物理CPU。虚拟机或者进程等在队列中处于一个就绪状态,直到被调度到CPU资源，这个过程中的时间便是就绪时间。

### 获取方式

##### 命令Esxtop

可以在`VMWare ESX服务器`上使用命令`esxtop`获取该参数。

![esxtop](/img/in-post/Ready-Time-Of-Performance-Optimization-In-VMware/esxtop.jpg)

- CORE UTIL。有该字段，说明开启了CPU超线程技术(HT)

- 主要的关注为`%RDY`这一栏

- 输入c,切换到cpu面板

- 输入m，切换到memory面板

- 输入i，切换到interrupts(中断)面板

- 输入d，切换到disk adapter(磁盘适配器)面板

- 输入u，切换到disk device(磁盘设备)面板

- 输入v，切换到disk VM(磁盘虚拟机)面板

- 输入p，切换到power states(电源管理)面板

- 输入R，在cpu面板上，%RDY值由大到小进行排序

- 输入2，向下一行高亮

- 输入8，向上一行高亮

##### 工具VisualEsxtop

下载地址: [VisualEsxtop](https://labs.vmware.com/flings/visualesxtop)

解压，打开解压缩后的文件夹，双击和运行`vtop.bat`(需要电脑中有java)


![VisualEsxtop](/img/in-post/Ready-Time-Of-Performance-Optimization-In-VMware/vtop-screenlarge.jpg)

- 设置刷新时间。点击`Configuration`，选择`Change Interval`，输入`2`(esxtop最短的刷新间隔为2秒)

- 筛选。连接上`ESX Host`后，选择`Chart`-`Object Types`-`Group`，通过对应的`GID`值，查找对应的监控程序。




### %RDY取值范围

| %RDY区间 | 关注度 | 说明 |
| :-----: | :---: | :---: |
| %RDY == 0 | 不会发生 | 由于客户机操作系统与真实硬件之间的虚拟化层VMM的存在，任何操作情况下，此值不可能为0。 一个健康的系统，此值小到以至于终端用户感知不到他们的业务是在虚拟化环境下运行的 |
| 0 < %RDY <= 5% | 正常区间 | 非常小，ready值意味着对用户体验非常小。如果系统存在性能问题，并且ready值在此区间，应为其它问题导致 |
| 5% < %RDY <= 10% | 值得关注 | 大多数系统功能在此区间内可以正常工作 |
| %RDY > 10% | 必须关注 | 尽管系统能够继续满足性能期望，但此时多数情况下需要采取措施来解决性能问题 |

### CPU scheduler

[The CPU Scheduler in VMware vSphere 5.1](https://www.vmware.com/techpapers/2013/the-cpu-scheduler-in-vmware-vsphere-51-10345.html)

> The CPU scheduler is an essential component of vSphere 5.x. All workloads running in a virtual machine must be scheduled for execution and the CPU scheduler handles this task with policies that maintain fairness, throughput, responsiveness, and scalability of CPU resources. 

### %RDY过高原因

- 大量CPU使用

    当另一台虚拟机开始运行时，会大量使用CPU，这时候%RDY值变高

- 资源消费者过多

    当寄主机负载过多数目的虚拟机，调度器始终忙于将即将运行或排到的虚拟机一个个排队

- 负载关联

    负载具有关联性。例如头一个负载结束后关联另一个负载启动，这不会产生过高的就绪时间。但是如果关联数目大的负载启动，就会产生就绪时间

- 虚拟机中虚拟CPU数量

    对于n路SMP系统虚拟机进行协同调度，虚拟CPU只有在n个物理CPU被获得时才会被调度

还有一些因素会影响就绪时间。例如：

- 被调度到特定的CPU上的虚拟机会更容易再被调度到相同的CPU，这是由于当前CPU含有数据缓存对高性能更有优势。

- ESX服务器调度器更愿意让CPU处于idle状态，而不是匆忙的将从一个CPU调度到另一个可能空闲的CPU上，真正的调度会在调度算法认可的情况下进行。



### 参考博文

1. [利用VisualEsxtop工具图形化查看esxtop参数](http://blog.51cto.com/huanwenli/1749214)
2. [CPU性能分析与监控之就绪时间(ready time)分析](http://blog.csdn.net/jinguangliu/article/details/38340989)
3. [Ready Time](https://communities.vmware.com/docs/DOC-7390)
4. [High CPU Ready, Poor Performance](http://vmtoday.com/2010/08/high-cpu-ready-poor-performance/)
5. [CPU Ready Revisted – Quick Reference Charts](http://vmtoday.com/2013/01/cpu-ready-revisted-quick-reference-charts/)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2018/03/21/Ready-Time-Of-Performance-Optimization-In-VMware/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
