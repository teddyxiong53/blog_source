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

lxk0301的docker目录下，docker-entrypoint.sh，是靠crond -f 来指定crond前台运行来保证不退出的。



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

属于s6项目的衍生项目。

# s6-svscan

这个是一个类似于supervisord的进程管理软件。

对进程进行监控，并进行重启等操作。

为什么不直接用supervisord呢？

因为supervisord默认不显示程序的打印日志，这个给docker的日志管理带来了麻烦。

怎么进行使用呢？

直接在dockerfile里加上这样一行：

```
add https://github.com/just-containers/s6-overlay/releases/download/v2.2.0.3/s6-overlay-amd64.tar.gz  /usr
```

这个会自动下载解压到/usr目录下。

每个要运行的程序，都单独创建一个目录。然后在里面新建一个名为run和一个名字为finish的脚本。

例如下面这样：

```
/service
    /app1
        /run
        /finish  ：可选的，主要用来进行资源清理。
    /app2
        /run
        /finish
```

然后容器启动时，设置这个

```
cmd ["/usr/bin/s6-svscan", "/service"]
```

这样容器启动的时候，就会扫描/service目录下的目录，并执行run脚本。

如果你不想app2被启动，那么就在app2目录下，放一个名为down的空文件就好了。

在nevinee的jd容器里，ps查看到的s6-svscan是这样的

```
s6-svscan -t0 /var/run/s6/services
```

看看/var/run/s6/services目录。

```
root@jd:/var/run/s6/services $ ls -a
.  ..  .s6-svscan  crond  refresh-cron  s6-fdholderd
```

s6-supvervisor的执行逻辑大概是这样的：

1、s6-supervisor把目录切换到service对应的目录下。例如上面的app1下面。

2、如果已经有另外一个s6-supervisor在监听这个服务了。那么直接退出，返回100这个错误码。

3、执行app1下面的run脚本。

4、run脚本应该阻塞的，不应该退出。

5、如果run脚本退出了，s6-supervisor会执行finish脚本（如果提供了这个脚本的话）。finish脚本不应该阻塞，很快执行完。

6、当finish脚本执行完了，s6-supervisor会执行run脚本。

7、s6-supervisor的行为，靠s6-svc来控制，相当于C/S架构。

s6-supervisor它不应该被手动执行，而是应该被它自己的supervisor（套娃了，哈哈），也是s6-svscan来启动。

# s6

s6是一套软件。

它的代码仓库是这里。

https://github.com/skarnet/s6

s6这个名字，估计是指代skarnet。s后面刚好是6个字母。

当前版本是2.10.0.3

代码看起来没有很复杂。

[s6-svscan](https://skarnet.org/software/s6/s6-svscan.html) and [s6-supervise](https://skarnet.org/software/s6/s6-supervise.html) are the long-lived processes maintaining the supervision tree. Other programs are a user interface to control those processes and monitor service states.

### Why "s6" ?

官方是这样递归的定义。

**s**karnet.org's **s**mall and **s**ecure **s**upervision **s**oftware **s**uite.

Also, s6 is a nice command name prefix to have: it identifies the origin of the software, and it's short. Expect more use of s6- in future skarnet.org software releases. And please avoid using that prefix for your own projects.



包括了这些软件

```
skalibs 
execline
s6
s6-portable-utils
s6-linux-utils
s6-dns
s6-networking
s6-rc
```

ska是开发这个软件的公司的名字。





# 参考资料

1、如何在一个Docker中运行多个程序进程

https://www.iamle.com/archives/2241.html

2、使用 s6-svscan 进行进程管理，docker supervisord 替代者

https://blog.csdn.net/shida_csdn/article/details/79361114

3、官网

https://skarnet.org/software/s6/s6-svscan.html