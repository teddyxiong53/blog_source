---
title: nodejs之child_process
date: 2018-12-19 15:04:17
tags:
	- nodejs

---



nodejs是以单线程模式运行的，使用事件驱动来处理并发。

在多核CPU上，我们可以用多进程来提高性能。

每个子进程总是带有3个流对象：child.stdin、child.stdout、child.stderr。

他们可能会共享父进程的stdio流，也可能是独立的被导流的对象。

nodejs提供了child_process模块来创建子进程。

方法有：

1、exec。

2、spawn。

3、fork。

# exec



# 参考资料

1、Node.js 多进程

http://www.runoob.com/nodejs/nodejs-process.html