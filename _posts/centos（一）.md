---
title: centos（一）
date: 2018-01-31 17:47:46
tags:
	- Linux
	- centos

---



对于红帽系列的linux一直没怎么用过。所以现在要把centos用起来。毕竟这个在服务器领域是很主流的。

# 下载安装

1、iso文件800M作用。安装有图形界面，感觉比Ubuntu的还简洁直观一些。64位的。

2、安装后，大概占用了1G空间，默认的安装把你的硬盘评分了2块，一半给根目录，一半给home目录。

3、看到内核版本是3.10的。

# 基本环境配置

1、我首先就是看ip地址，方便通过ssh访问。但是一上来，就遇到一个下马威，居然没有ifconfig命令。

2、但是联网是通的。所以可以先安装一下ifconfig。

3、说到安装软件，我首先想到的就是像debian那样配置软件源。但是看了一下，好像centos没有这种概念。网上说可以先安装一个加速器。

```
yum install yum-fastestmirror
```

这个会自动帮你找到最快的镜像站点镜像软件下载。

从结果看，它找到了163的、aliyun的站点。的确下载软件的速度特别快。满速的。

安装net-tools。

```
yum install net-tools
```

4、安装ssh server。加-y选项，就不用在安装过程中确认了。

```
yum -y install openssh
```

安装 后，默契启动服务。你可以从pc上连接过来了。

# yum命令学习

把常用的了解一下。

1、安装软件。

```
yum install -y xxx
```

2、卸载软件。

```
yum remove  xxx
```

3、查找软件。

```
yum search xxx
```

4、更新。

```
yum update
yum upgrade
```

5、查看系统信息。

```
yum version
[teddy@localhost /]$ yum version
Loaded plugins: fastestmirror
Installed: 7/x86_64                 
Group-Installed: yum                
version
```

可以看到这里有个插件的概念。

## yum插件

yum本身功能不怎么样，但是可以通过插件来扩展。

# 配置samba服务

1、安装。

```
yum install -y samba
```

2、配置。

我按照我在Ubuntu上一贯的配置。

练级不上。先不管。

