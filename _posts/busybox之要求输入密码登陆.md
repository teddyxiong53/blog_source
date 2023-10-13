---
title: busybox之要求输入密码登陆
date: 2018-01-29 23:24:38
tags:
	- busybox
---

--

我的目的是研究怎么自动登陆。或者延迟登陆shell。加快开机速度。

直接运行-sh不就好了吗？

```
# now run any rc scripts
::respawn:-/bin/sh
::sysinit:/etc/init.d/rcS
```

就这样是可以的正常的。



要输入密码进入登录的是这样的：

```
::respawn:/sbin/getty -L ttyAMA0 115200 vt100
```

是调用了getty。这个就会提示登录。这里如果验证通过，会调用/bin/sh。

不要登录的是这样的：

```
ttyS0::respawn:-/bin/sh
```

是直接调用/bin/sh了。

如果要登录，其实还需要做一件事。就是在/etc/目录下添加group、shadow、passwd这3个文件。

一般做法是把你的host机器里的文件拷贝进来就好了。

要密码的passwd文件内容：

```
root:x:0:0:root:/root:/bin/sh
```

不要密码的passwd文件内容：

```
root::0:0:root:/:/bin/sh
```

区别就在于root后面那个x，有x，要密码，没有x，不要密码。

如果你把group、shadow、passwd文件都拷贝进来了。又不想要输入密码，可以这样做：

```
1、passwd里把root后面那个x删掉
2、把shadow文件删掉。因为这里面存了加密的密码。
```



bash进程来源于login进程，login进程来源于getty进程或者telnetd进程，从上图中可以看到，bash进程在启动之后，首先加载一系列的配置，最后阶段就readloop，循环等待/dev/tty是否有读数据，也就是看下终端是否有输入的命令。如果有输入就通过flex bison来解析数据，然后看下是否要去fork子进程去执行任务。

 bash进程会把当前的终端和fork出来的子进程做一下关联，这个过程就是进程组获得了控制终端的过程。

参考资料

1、控制终端与前台进程组

http://blog.chinaunix.net/uid-30485355-id-5301998.html

2、

https://zhidao.baidu.com/question/1924322162402419187.html

3、root自动登陆(busybox

http://blog.sina.com.cn/s/blog_735da7ae0102v2o0.html