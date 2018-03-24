---
title: kvm（一）
date: 2018-03-24 09:35:33
tags:
	- kvm

---



这个打算写成系列文章。把kvm这个点梳理清楚。

# 概念

kvm是Kernel Virtual Machine的意思，表示内核虚拟机。

kvm要求cpu必须支持硬件虚拟化。

怎么查看？

输入这个命令。

```
teddy@teddy-ubuntu:~$  egrep -o 'vmx | svm' /proc/cpuinfo | wc -l
4
```

只要输出的不是0，说明是支持的。我是在VMware里的Ubuntu里看的。

我的机器本来输出是0。需要设置虚拟机- 处理器 -虚拟化引擎，勾选虚拟化Intel-VT。

然后就好了。



# 安装配置

1、安装kvm相关软件包。

```
sudo apt-get -y kvm virt-* libvirt bridge-utils qemu-img
```



# 参考资料

1、kvm使用入门详解

https://www.cnblogs.com/liwei0526vip/archive/2016/12/20/6201582.html

