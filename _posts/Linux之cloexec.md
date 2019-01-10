---
title: Linux之cloexec
date: 2019-01-10 14:17:51
tags:
	- Linux
---



什么是cloexec？

是close on execute的缩写。

应对的是这样的场景：

在exec启动新进程后，子进程仍然可以操作父进程里的fd。

很多时候，我们不希望这样。

所以就希望在exec的时候，子进程关闭掉这些fd。

要达到目的，有两种方法：

1、O_CLOEXEC。在open的时候，就传入这个标志。这个是Linux2.6之后才执行的。

2、F_CLOEXEC。专门用fcntl函数来给fd进行操作。





参考资料

