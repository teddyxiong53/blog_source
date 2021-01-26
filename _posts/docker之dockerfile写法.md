---
title: docker之dockerfile写法
date: 2021-01-21 11:00:11
tags:
	- docker

---

--

dockerfile本质上是脚本文件。

被docker程序来解释执行。

构成是一条一条的指令。

每条指定对应Linux下的一条命令。

类似于Makefile。

docker程序根据Dockerfile，生成镜像。

指令忽略大小写。

建议使用大写。

使用`#`作为注释。

# 指令分类

指令分为两种：

1、build指令。

2、run指令。

build指令用于构建镜像。只在构建的时候起作用，在容器运行的时候，就不起作用。

而run指令，用来设置镜像的属性，在容器运行时执行。



Dockerfile中包括FROM、MAINTAINER、RUN、CMD、EXPOSE、ENV、ADD、COPY、ENTRYPOINT、VOLUME、USER、WORKDIR、ONBUILD等13个指令

![å¨è¿éæå¥å¾çæè¿°](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/20200215111457987.png)

# build类型指令

## from指令

这个必须放在最前面。

表示基于的镜像。

后面可以是本地的镜像，也可以是远程的镜像。

格式：

```
from <image>:<tag>
```

举例：

```
from hub.c.163.com/netease_comb/debian:7.9
from node:lts-alpine
```

## maintainer指令

docker inspect的时候，会显示镜像的这个信息。

一般这样写：

```
maintainer teddyxiong53 <1073167306@qq.com>
```

## run指令

run就是执行Linux的命令。

这个就依赖于基础镜像支持哪些命令了。

## add指令

从主机复制文件到容器的路径上。



## workdir

设置工作目录。



## arg指令

这个估计是后面新增的指令。

是设置一个shell变量。方便后面进行使用。

在build的过程中使用。



# run类型指令

## cmd指令

容器启动的时候执行的操作。

在一个dockerfile里，只能出现一次。

如果有多次，只有最后一次有效。

## entrypoint

也是在容器启动的时候执行。

也是只出现一次，多次的话，只有最后一个有效。

有两种用法：

```
1、单独用。
	如果另外还有cmd指令，而且cmd指令有效。
	那么entrypoint和cmd会相互覆盖。后面的有效。
2、跟cmd指令配合使用。
	这样cmd就不能是完整的指令，只有参数部分。
```

## expose指令

映射容器的某个端口到主机。

## env

设置环境变量

```
env PATH=/usr/local/bin SHELL=/bin/bash 
```

## volume指令

设置挂载点。





![å¨è¿éæå¥å¾çæè¿°](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/20200215130213232.png)

参考资料

1、dockerfile简介及书写规则

https://www.cnblogs.com/ZCQ123456/p/11918470.html

2、

https://blog.csdn.net/qq_41094332/article/details/104324620

3、

https://www.cnblogs.com/jiangbo44/archive/2004/01/13/14117328.html

