---
title: Linux之start-stop-daemon
date: 2018-06-28 19:10:28
tags:
	- Linux

---

1

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

