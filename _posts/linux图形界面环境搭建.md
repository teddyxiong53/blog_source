---
title: linux图形界面环境搭建、
date: 2018-12-26 20:03:45
tags:
	- linux

---



在使用了Linux这么久之后，我觉得可以让Linux在我的生活中占据更加重要的地位了。

可以慢慢地把更多的事情放到linux上去做。甚至基本取代windows，作为我的主力操作系统。

当前我并不需要多台高性能电脑。所以还是通过虚拟机的方式进行解决。

虚拟机，我选择virtualbox，因为这个使用上可以跟主机系统无缝切换，这个提体验比VMware要好很多。

系统我选择xubuntu18.04  64位。既然是全新安装，那就选择最新的版本。

界面我就跟定了xfce。

这次我把硬盘分大一些，直接给500G。

我会更多地在这个虚拟机里进行开发工作，包括连接usb外设进来的那种涉及硬件的。

分配3张网卡：

1、host only的。

2、nat。

3、桥接的。



这个版本的已经对win键有不少支持了。

可以win+方向左/右进行操作了。

更新源。

```
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
```

然后update和upgrade。



安装开发工具。

vscode，直接下载deb包安装就好了。

```
sudo apt-get install git gcc cmake build-essential
```



我安装samba一直不行。

事实证明，跟太新的版本，要付出代价的。删掉这个版本，回到Ubuntu16.04的。自己安装xfce桌面。





