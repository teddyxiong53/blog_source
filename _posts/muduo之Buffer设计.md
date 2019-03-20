---
title: muduo之Buffer设计
date: 2019-03-20 16:14:32
tags:
	- cpp

---





为什么non-blocking网络编程里，应用层Buffer是必须的？

```
non-blocking的核心思想是：避免阻塞在read/write上。
这样可以最大限度地使用这个控制线程。
让该线程可以服务于更多的socket连接。
io线程只能阻塞在select上（下面select/poll/epoll都简写为select，他们性质相同）。
这样一来，应用层的缓冲是必须的。
每个tcp socket都要有stateful的input buffer和output buffer。
```



考虑一个常见的场景：

程序要通过tcp连接发送100K的字节数据。但是在write这个syscall里，os只接受了80K字节。

（这个是受tcp advertised window的控制）。

你肯定不想在原地等待，这个时间取决于对方接受数据，然后本机滑动窗口。

程序应该尽快交出控制器，返回event loop。

在这种情况下，剩下的20k数据怎么办？



对于应用程序而言，它只管生成数据，而不应该关心数据是分几次发送的，这些应该由网络库来做。

应用只需要调用TCPConnection::send函数就可以了。

网络库应该接管剩余的20K数据，保存在TcpConnection的output buffer里。

然后注册POLLOUT事件，一旦socket变得可用，马上发出去。

一旦数据发送完成，就要停止关注POLLOUT，以免造成busy loop。

（因为muduo里用的是epoll的电平触发的）。

如果这个时候，应用又写入了50K数据，应该排队到前面那20K的后面。



muduo里的Buffer类似一个queue，从后面写入，从前面读取。

那么设计Buffer的时候，大小怎么考虑呢？

希望可以减少系统调用次数，那么就应该把buffer给大一些。

但是buffer给大了，又会占用较多内存。

muduo是使用readv函数结合栈上空间来解决的。



参考资料

1、Muduo 设计与实现之一：Buffer 类的设计

https://blog.csdn.net/Solstice/article/details/6329080

2、Muduo 网络编程示例之零：前言

可以顺着这篇文章看这个系列的。

https://blog.csdn.net/Solstice/article/details/6171831