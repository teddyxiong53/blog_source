---
title: Linux之作业控制
date: 2017-08-05 23:30:38
tags:

	- Linux

---

Linux下没有像windows下那样的任务栏，多个任务直接怎样进行方便快捷的切换呢？现在就来讨论这个问题。

Linux里作业有前台、后台的概念。前台执行的程序会占用当前shell的输入和输出。后台运行的方法就是在命令最后加上一个`&`。

我们输入下面命令：

```
sleep 2000
```

糟糕，这个命令运行很久，占据了我们的shell，我们想让它转到后台去运行，怎么操作？

输入ctrl+z就行。但是好像有点不对。怎么变成停止状态了呢？

```
teddy@teddy-ubuntu:/etc/udev/rules.d$ sleep 2000
^Z
[1]+  已停止               sleep 2000
```

我们想让这个任务在后台继续运行，怎么做？用bg命令就可以。

```
teddy@teddy-ubuntu:/etc/udev/rules.d$ jobs
[1]+  已停止               sleep 2000
teddy@teddy-ubuntu:/etc/udev/rules.d$ bg 1
[1]+ sleep 2000 &
teddy@teddy-ubuntu:/etc/udev/rules.d$ jobs
[1]+  运行中               sleep 2000 &
```

jobs命令的作用就有点像windows下的任务栏了。那我想把某个任务转到前台来，该怎么做？用fg命令。

我们当前在用vi编辑文件，用ctrl+z退出来了。现在想要继续。用`fg 2`就可以了。2是jobs看到内容的第一列的任务号。

```
teddy@teddy-ubuntu:~$ jobs
[1]-  运行中               sleep 2000 &  (工作目录: /etc/udev/rules.d)
[2]+  已停止               vi test.c
```

