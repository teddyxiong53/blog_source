---
title: busybox之要求输入密码登陆
date: 2018-01-29 23:24:38
tags:
	- busybox
---



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

