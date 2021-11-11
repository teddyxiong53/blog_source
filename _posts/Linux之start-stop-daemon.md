---
title: Linux之start-stop-daemon
date: 2018-06-28 19:10:28
tags:
	- Linux

---

--

作用：用来启动或者停止一个daemon程序。

一般用来保证程序只被启动一次。



一个例子。

```
start-stop-daemon -S -q -m -p $TEST_MAIN_PIDFILE -b -x $TEST_MAIN_DAEMON
```

命令基本格式：

```
start-stop-daemon [<option> ...] <command>
```

cmd有：

```
-S
	等于--start，启动一个程序，并把参数传递给它。
-K
	等于--stop，
--T
	等于--status，获取程序的状态。

```

常用选项：

```
-q：quiet，安静。
-m：创建pid文件，在启动之前。
-p：启动前检查pid文件。
-b：后台模式。
-x：可执行程序。
```



返回值：

```
0：成功。
1：什么也没做。
2：
3：出错
```



# 问题

## snapserver启动失败

命令展开是这样：

```
start-stop-daemon --start --quiet --pidfile /var/run/snapserver/pid --exec /usr/bin/snapserver -- 
```

最后多的这个`--`是干啥的？

完全没有影响。应该是被忽略掉了。

手动执行这个是可以的。

在脚本里，加上`-b`选项就正常了。

那就是这个导致的。

不对，虽然返回值是正常的。但是进程还是没有起来。

去掉最后的--，就可以。

但是snapclient也有--，为什么可以起来？

