---
title: Linux内核之namespace
date: 2018-03-18 11:07:43
tags:
	- Linux
---

--

namespace是一种机制，用来对系统的全局资源进行隔离。

哪些资源是可以隔离的？有这些：

```
1、进程间通信。
2、主机名。
3、进程id。
4、网络资源。
	接口、协议栈、路由表。
5、mount。
6、用户和组。
```

启用namespace机制后，就对上面这些资源进行了隔离。

怎么查看namespace呢？

/proc/xx/ns目录下，可以查看。xx表示某一个进程号。

```
hlxiong-VirtualBox# ls -lh
总用量 0
lrwxrwxrwx 1 root root 0 12月  7 14:37 cgroup -> cgroup:[4026531835]
lrwxrwxrwx 1 root root 0 12月  7 14:37 ipc -> ipc:[4026531839]
lrwxrwxrwx 1 root root 0 12月  7 14:37 mnt -> mnt:[4026531840]
lrwxrwxrwx 1 root root 0 12月  7 14:37 net -> net:[4026531993]
lrwxrwxrwx 1 root root 0 12月  7 14:37 pid -> pid:[4026531836]
lrwxrwxrwx 1 root root 0 12月  7 14:37 pid_for_children -> pid:[4026531836]
lrwxrwxrwx 1 root root 0 12月  7 14:37 user -> user:[4026531837]
lrwxrwxrwx 1 root root 0 12月  7 14:37 uts -> uts:[4026531838]
```

下面我们看看主机名的设置。

我们另外开一个shell窗口。

执行：

```
unshare -u
```

然后修改hostname：

```
hostname mypc
```

然后看另外一个shell窗口里的hostname，还是保持之前的没有改变。



unshare命令用法

```
-m
	修改mount。
-u
	修改uts
-i
	修改ipc
-n
	修改net。
-p
	修改pid。
-U
	修改user。
	
```



修改uts的这个特性，在docker里用到了。

这个特性可以让子进程拥有独立的主机名和域名。





参考资料

1、Linux namespace机制

https://blog.csdn.net/quakedinosaur/article/details/87899253

2、Linux UTS namespace 隔离

https://my.oschina.net/javamaster/blog/1782839