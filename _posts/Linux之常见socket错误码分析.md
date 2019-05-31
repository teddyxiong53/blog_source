---
title: Linux之常见socket错误码分析
date: 2017-09-22 19:48:46
tags:
	- Linux

---



read函数分析

```
nread = read(sockfd, buf, buflen);
```

过程：

1、nread > 0。

读取正常。

2、nread == 0 。

套接字关闭。break处理。

3、nread < 0

需要判断返回值。

EINTR、EWOULDBLOCK、EAGAIN。这3个 都是正常的。continue处理。

EWOULDBLOCK==EAGAIN。表示的都是阻塞模式下，要读取，但是当前还没有数据。

EINTR表示操作被中断。



我还是以send和recv作为分析对象吧。

send

```
返回值：
成功的时候，返回的是发出去的字节数。
失败的时候，返回-1。具体错误信息通过errno来体现。

错误码
EAGAIN or EWOULDBLOCK
	当socket被设置为非阻塞模式时，当前buffer是满的，无法发送。
	这种处理，应该是continue。
	
ECONNRESET
	连接被对方reset了。
EINTR
	这个是被signal打断了。可以continue。
	这个也是阻塞的时候，进程收到一个signal，阻塞接口继续执行，就是对应这个错误。
```

recv

```
返回值规律跟send一样。
有一点不一样，就是返回值为0，表示读取完了。
```



recv等待对方的数据时，没有收到。

```
[11]:[Resource temporarily unavailable]
```

EAGAIN就是11 。



# EINTR

阻塞的操作被取消阻塞的调用打断。例如设置了发送接收超时，就会遇到这种错误。

只对于设置了BLOCK模式的socket会出现。



# ETIMEOUT

1、操作超时。一种常见的用法是：发送后，会设置接收的超时时间，设定时间内没有得到回答，就报这个错误。

2、一般是在服务器端程序崩溃了，客户端会出现这种错误。

客户端的tcp会在一定时间内持续重发数据，试图从服务端获得一个ACK，最后还是不行，客户端就报了这个错了。



# EAGAIN

字母含义，再来一次。

1、send函数返回值比发送的数据字节数要少。会返回EAGAIN和EINTR。

2、recv函数返回值小于要读的字节数时。再次读有可能会触发这个错误。

3、socket没有设置为阻塞模式，写缓存队列是满的，你要去发送，就会报这个。处理方法是等会儿再发。



# EWOULDBLOCK

期望阻塞。

资源暂时不可用。这个一般是在socket是非阻塞模式时出现。

不是严重错误。

# EPIPE

如果一个socket被关闭了。还是视图用对应的fd进行send或者recv，就会报这个错误。

这个错误会触发SIGPIPE，系统对SIGPIPE的模式处理是杀掉该进程。

而一般出现这个错误，并没有那么严重，所以一般进程都会自己捕获这个SIGPIPE，避免一不小心就被杀死。





# 参考资料

1、一篇文章完全搞清楚 scoket read/write 返回码、阻塞与非阻塞、异常处理 等让你头疼已久的问题

https://www.cnblogs.com/junneyang/p/6126635.html