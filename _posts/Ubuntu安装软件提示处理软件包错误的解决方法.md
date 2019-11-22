---
title: Ubuntu安装软件提示处理软件包错误的解决方法
date: 2017-06-12 19:31:04
tags:

	- ubuntu

---

要在Ubuntu下安装lxc，Ubuntu版本是12.04，看网上的相关教程都没有提到安装lxc会出错的，但是我安装就是不成功。提示出错信息如下：

```
正在设置 lxc (1.0.10-0ubuntu1) ...
dpkg: 处理软件包 lxc (--configure)时出错：
 子进程 已安装 post-installation 脚本 返回错误状态 1
dpkg: 依赖关系问题使得 lxc-templates 的配置工作不能继续：
 lxc-templates 依赖于 lxc (>= 0.8.0~rc1-4ubuntu43)；然而：
  软件包 lxc 尚未配置。

dpkg: 处理软件包 lxc-templates (--configure)时出错：
 依赖关系问题 - 仍未被配置
正在设置 python-distro-info (0.12) ...
因为错误消息指示这是由于上一个问题导致的错误，没有写入 apport 报告。
```

网上找到一篇文章，有提到解决类似问题的一种方法，我试了下，有用。方法如下：

## 1. 备份目录

```
mv /var/lib/dpkg/info /var/lib/dpkg-bak-20170612
```

这个目录在我的系统，当前是67M大小。

## 2. 创建新的空目录 

```
mkdir /var/lib/dpkg/info
```

## 3. 再次进行安装

```
sudo apt-get install lxc
```

这样就没有提示之前的错误了。



但是后续我安装其他的程序的时候，提示了一堆的错误。所以其实还需要执行一下`sudo apt-get update`。



#一个错误解决办法

正试图覆盖 /usr/share/accounts/services/google-im.service,它同时被包含于软件

```
sudo apt-get -o Dpkg::Options::="--force-overwrite" -f install
```

