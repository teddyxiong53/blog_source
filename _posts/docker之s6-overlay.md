---
title: docker之s6-overlay
date: 2021-05-10 19:26:34
tags:
	- docker
---

--

看nevinee的jd docker镜像，有点特别，使用了s6-overlay这个东西。

s6-overlay是什么？做什么用的？



我们都知道Docker容器的哲学是一个Docker容器只运行一个进程,

但是有时候我们就是需要在一个Docker容器中运行多个进程

那么基本思路是在Dockerfile 的CMD 或者 ENTRYPOINT 运行一个”东西”,

然后再让这个”东西”运行多个其他进程

**简单说来是用Bash Shell脚本或者三方进程守护 (Monit,Skaware S6,Supervisor),**

其他没讲到的三方进程守护工具同理



# shell脚本的方式

入口文件运行一个Bash Shell 脚本, 然后在这个脚本内去拉起多个进程
注意最后要增加一个死循环不要让这个脚本退出,否则拉起的进程也退出了

```
#!/bin/bash

# start 1
start1  > /var/log/start1.log 2>&1 &
# start 2
start2 > /var/log/start2.log 2>&1 &

# just keep this script running
while [[ true ]]; do
    sleep 1
done
```



# 三方进程守护之-Skaware S6

Supervisor是常见的进程守护程序，

不过程序文件太大，

想要容器镜像尽量小,

在特别是用Alpine作为基础镜像的时候推荐使用Skaware S6

参考这个微服务基础镜像 https://github.com/nicholasjackson/microservice-basebox 

他就是用 Skaware 作为进程守护程序运行多个进程的

如果基础容器镜像是本身就是Alpine,那就再合适不过了

# s6-overlay代码

代码在这里：

https://github.com/just-containers/s6-overlay

s6-overlay-builder是一系列的init脚本和工具，用来简化用s6作为supervisor的方式创建docker镜像。



参考资料

1、如何在一个Docker中运行多个程序进程

https://www.iamle.com/archives/2241.html

