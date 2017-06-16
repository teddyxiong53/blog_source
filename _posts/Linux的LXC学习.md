---
title: Linux的LXC学习
date: 2017-06-06 22:26:26
tags:

	- Linux
	- lxc

---

容器的概念在最近几年因为docker的流行变得为大家都熟知。而实际上Linux的早期容器是lxc。

lxc是Linux Container的缩写。

对于普通用户来说，容器有什么用途呢？我觉得可以把容器看做一种更轻量级的虚拟机。有了容器，我们在Linux上体验其他的发行版本，就可以变得非常容易。

先不多说概念，先来一个实际操作，增加感性认识。

安装lxc：

```
sudo apt-get install lxc
```

我的Ubuntu安装会提示一个错误，哦在另外一篇文章了提到了解决方法。

然后运行lxc-checkconfig。

```
teddy@teddy-ubuntu:~$ lxc-checkconfig 
Kernel configuration not found at /proc/config.gz; searching...
Kernel configuration found at /boot/config-4.2.0-16-generic
--- Namespaces ---
Namespaces: enabled
Utsname namespace: enabled
Ipc namespace: enabled
Pid namespace: enabled
User namespace: enabled
Network namespace: enabled
Multiple /dev/pts instances: enabled

--- Control groups ---
Cgroup: enabled
Cgroup clone_children flag: enabled
Cgroup device: enabled
Cgroup sched: enabled
Cgroup cpu account: enabled
Cgroup memory controller: enabled
Cgroup cpuset: enabled

--- Misc ---
Veth pair device: enabled
Macvlan: enabled
Vlan: enabled
Bridges: enabled
Advanced netfilter: enabled
CONFIG_NF_NAT_IPV4: enabled
CONFIG_NF_NAT_IPV6: enabled
CONFIG_IP_NF_TARGET_MASQUERADE: enabled
CONFIG_IP6_NF_TARGET_MASQUERADE: enabled
CONFIG_NETFILTER_XT_TARGET_CHECKSUM: enabled

--- Checkpoint/Restore ---
checkpoint restore: enabled
CONFIG_FHANDLE: enabled
CONFIG_EVENTFD: enabled
CONFIG_EPOLL: enabled
CONFIG_UNIX_DIAG: enabled
CONFIG_INET_DIAG: enabled
CONFIG_PACKET_DIAG: enabled
CONFIG_NETLINK_DIAG: enabled
File capabilities: enabled

Note : Before booting a new kernel, you can check its configuration
usage : CONFIG=/path/to/config /usr/bin/lxc-checkconfig
```

lxc的相关命令有这些：

```
teddy@teddy-ubuntu:~$ lxc-
lxc-attach           lxc-clone            lxc-destroy          lxc-info             lxc-start            lxc-unshare
lxc-autostart        lxc-config           lxc-device           lxc-ls               lxc-start-ephemeral  lxc-usernsexec
lxc-cgroup           lxc-console          lxc-execute          lxc-monitor          lxc-stop             lxc-wait
lxc-checkconfig      lxc-create           lxc-freeze           lxc-snapshot         lxc-unfreeze  
```

简单起见，我们创建一个busybox的容器。

容器的模板在/usr/share/lxc/templates下面。

```
# 创建容器
# sudo lxc-create -n my_lxc_busybox -t busybox
```

然后尝试去启动这个容器。

` sudo lxc-start -n my_lxc_busybox `

结果提示virbr0找不到，这个确实是我系统当前的问题。上网查了下，发现是需要安装libvirt。于是再安装：

`sudo apt-get install virtinst  `

现在ifconfig就可以看到虚拟网卡已经出来了。

默认下载会到官网上去下载。比较慢。可以指定下载地址如下：

```
sudo MIRROR="http://ftp.cuhk.edu.hk/pub/Linux/ubuntu" \
     SECURITY_MIRROR="http://ftp.cuhk.edu.hk/pub/Linux/ubuntu" \
     lxc-create -n mylxc -f lxc.conf -t ubuntu -- -r trusty
```





