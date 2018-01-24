---
title: docker之学习（一）基础概念
date: 2018-01-22 10:12:26
tags:
	- docker
typora-root-url: ..\
---



# docker出现的历史背景

2010年之后，服务器市场开始急速向云环境转移。物理服务器的采购安装流程是很长的，相比之下，云服务器只需要点击几次鼠标就可以了。

服务器的扩展虽然简单了，但是在服务器上安装自己的软件服务还是很麻烦。虽然开源借助shell来实现一定的自动化。但是这种方法还是有很大的局限性。很难实现集中式管理。

这个时候，产业界出现了“不可变基础设施”这个新概念。指的是主机os和服务运行环境分离，只设置一次环境，之后不发生变更。

不可变基础设施有很多好处：

1、管理方便。因为服务环境是以镜像的方式存在。一个环境是文件。文件就可以很方便的进行版本管理。

2、扩展方便。与云平台配合进行可伸缩配置。

3、方便测试。开发和测试的环境自然统一了。

4、轻量级。

docker就是不可变基础设施的一种实现。

从docker的logo上的鲸鱼驮着集装箱，可以把docker理解为集装箱。什么都可以往里面装。

docker借鉴了集装箱的概念。

# docker和虚拟机的关系

虚拟机从全虚拟，发展到半虚拟的Xen，docker是比半虚拟更加轻量的一种方式。

# docker与Linux系统的关系

docker利用了Linux的cgroup和namespaces来实现。

最开始，docker是基于LXC的，从0.9版本开始，开发了LXC的替代品libcontainer。

![/images/docker之学习-图1.png](/images/docker之学习-图1.png)

#docker镜像与容器

镜像和容器是docker里两个基础概念。

根据可执行程序和进程的概念来进行类比，镜像相当于可执行程序，容器相当于进程。

镜像运行后，就是一个容器了。一个镜像可以多次运行，形成多个实例。

镜像是构建docker世界的基石。

镜像代表一个只读的layer。layer是指容器文件系统中可叠加的一部分。

在进一步理解之前，我们先看看镜像相关的4个概念：rootfs、union mount、image和layer。

## rootfs

代表一个容器起来后，里面看到的文件系统。

传统的linux启动过程中，内核先挂载一个只读的rootfs。检测完整性之后，根据bootcmd决定是否切换为R/W模式。

docker架构下，docker daemon没有将container的文件系统设置为RW模式，而是利用union mount的技术，在只读的rootfs上挂载了一个RW的文件系统。挂载的时候，这个RW文件系统没有任何内容。

实现了这种union mount的文件系统，就叫做union filesystem。

AUFS就是一种union filesystem。

AUFS涉及的技术就是COW写时复制的特性。

cow文件系统和其他文件系统的最大区别就是：从不覆写已有文件系统的已有内容。这些东西全部靠内核来做，用户感觉不出来的。



## 镜像

镜像又有父镜像和基础镜像这2个概念。



## layer

在docker的术语中，layer和镜像是含义比较接近的词。

rootfs中每个只读的镜像都可以叫做一个layer。



#镜像大小情况

官方镜像很少基于Ubuntu，使用Debian多一些。现在很多官方镜像都往更加精简的alpine迁移。

先看一下os的大小情况。

```
Ubuntu:latest   187MB
debian:latest   125MB
centos:latest    196M
alpine           5M
```

可见，alpine很小。alpine是一个面向安全的轻型linux发行版。跟一般的linux发行版不同，alpine采用了musl libc和busybox。提供了包管理工具apk。这个包管理还是很强大的。

例如，这个安装了mysql的客户端，Dockerfile这样就可以了：

```
FROM alpine:3.3
RUN apk add --no-cache mysql-client
ENTRYPOINT ["mysql"]
```

但是是否需要很关注基础镜像的size，这也是一个值得讨论的问题。

小是alpine的最大优势，但是docker的文件系统可以进行分层缓存。对于已经拉取过镜像的机器来说，每次的增量更新内容并不多。也就是说，如果所有的镜像都使用相同的基础镜像，这个机器上都只会pull一次。



# docker带来的好处

1、提供了一种简单、轻量的建模方式。docker上手非常快，用户只需要几分钟就可以把自己的程序“docker化“。

2、职责的逻辑分离。用了docker之后，开发人员只需要关心容器里的应用，运维人员只需要关心如何管理容器。

3、鼓励使用面向服务的架构。

docker推荐一个容器只运行一个应用。这样就形成了一个分布式的应用程序模型。

# registry

registry的字面意思是挂号处。

docker用registry来保存用户构建的镜像。

registry分为共有和私有两种。

docker公司维护的公共registry就是docker hub。

用户可以在dockerhub网站上注册，分享保存自己的镜像。

用户还可以架设自己的本地registry。

#分析一个docker容器

```
docker run -i -t ubuntu:14.04
```

然后在起来的终端里看一些东西。

```
root@677da434144e:/# hostname
677da434144e
root@677da434144e:/# cat /etc/hosts
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.17.0.6      677da434144e
root@677da434144e:/# ifconfig 
eth0      Link encap:Ethernet  HWaddr 02:42:ac:11:00:06  
          inet addr:172.17.0.6  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:acff:fe11:6/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:27 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:3600 (3.6 KB)  TX bytes:648 (648.0 B)
```

可以看到有一个eth0，网段是172.17.0.6，对应的主机里有个叫docker0的网卡，ip是172.17.0.1 。

我们在这个容器内部的操作。可以在主机里，用docker logs xxx(xxx是指容器id)来看到。

```
teddy@teddy-ubuntu:~/work/test/exampleapp$ docker logs 677da434144e
root@677da434144e:/# 
root@677da434144e:/# uname
Linux
root@677da434144e:/# hostname
677da434144e
root@677da434144e:/# cat /etc/hosts
```

