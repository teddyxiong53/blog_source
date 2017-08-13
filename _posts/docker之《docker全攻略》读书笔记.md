---
title: docker之《docker全攻略》读书笔记
date: 2017-08-13 21:13:56
tags:

	- docker

---

# 1. docker的由来

谈到docker，就要先说LXC。LXC是Linux Container的缩写，是docker技术的基础。

CPU、内存、io、网络，这些都叫做系统资源。Linux内核管理这些系统资源是通过cgroups和namespaces来做的。

cgroups可以限制、记录、调整进程组所使用的物理资源。比如说，cgroups可以给某个进程组分配更多的CPU使用周期，也可以限制某个进程组的内存使用上限。有了cgroups，Linux内核虚拟化才有了可能。

namespaces则是另外一个重要的资源隔离机制。namespaces进程、进程组、ipc、网络、内存等资源变得不再是全局性资源，而是在内核层面上就属于某个特定的namespace。在不同的namespace之间，这些资源是互相透明的、不可见的。

LXC就是通过cgroup和namespace，在内核层面实现了轻量级的虚拟化。

LXC和docker是：

LXC的docker的基础，docker是LXC的一个杀手级应用。

# 2.docker为什么选在了AUFS

AUFS是Another Union FS的缩写。是对UnionFS的补充。但是UnionFS很久不更新了，所以就推出了AUFS了。

AUFS的功能简单说就是：可以将分布在不同地方的目录挂载到同一个vfs上。

# 3. docker的推出过程

2010年，dotCloud公司推出了docker，但是因为当时很多巨头进入到PAAS领域，该公司日子不好过，所以就把docker开源了。

docker的出现，让开发、测试、生产的环境统一了。

开源后，docker就一帆风顺了，巨头都宣布支持docker。

# 4. docker一般用在什么场景

云平台领域是docker的最佳使用场景。其意义相当于Java对于软件开发的意义一样，实现了跨平台。一次编写，处处运行。

docker的出现，让开发人员和运维人员都很高兴。这样就不会再出现环境不统一的问题了。

# 5. docker的优点和缺点

## 优点

1、docker比传统的虚拟机资源利用率要高。

2、支持跨节点部署。

3、版本可控，组件可复用。

4、共享镜像。

5、轻量，易维护。从内核的角度看，docker就是一个普通的进程。启动停止都是一瞬间完成。

## 缺点

1、宿主资源没有完全隔离，例如/proc、/sys等目录还是共享使用的。/dev也没有隔离，这些当前还没有爆发问题。

2、golang还不成熟。golang是docker的实现语言。

3、docker虽然开源，但是还是受一家商业公司控制，可能有商业风险。

# 6. docker未来怎么发展

在docker发布之前，几乎所有的云平台都是采用虚拟机的架构来部署应用。虚拟机包装的一个完整的“机器”。而docker包装的是一个应用。

在VMware推出的时候，大家都把它当做虚拟化工作站来用的，而现在VMware作为云平台的基础解决方案异军突起。而docker现在在走VMware走过的路。



# 7. docker的安装

注意事项：

1、用64位的Linux。

2、用root权限运行。

3、最好在Linux上用。

