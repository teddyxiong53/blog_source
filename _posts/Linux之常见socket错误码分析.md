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
首先阻塞接收的recv有时候会返回0，这仅在对端已经关闭TCP连接时才会发生。
而当拔掉设备网线的时候，recv并不会发生变化，仍然阻塞，如果在这个拔网线阶段，socket被关掉了，后果可能就是recv永久的阻塞了。
所以一般对于阻塞的socket都会用setsockopt来设置recv超时。
当超时时间到达后，recv会返回错误，也就是-1，而此时的错误码是EAGAIN或者EWOULDBLOCK，POSIX.1-2001上允许两个任意一个出现都行，所以建议在判断错误码上两个都写上。
```

```
一般设置超时的阻塞recv常用的方法都如下：
while(1)
{
    cnt = (int)recv(m_socket, pBuf,RECVSIZE, 0);
    if( cnt >0 )
    {
        //正常处理数据
    }
    else
   {
         if((cnt<0) &&(errno == EAGAIN||errno == EWOULDBLOCK||errno == EINTR)) //这几种错误码，认为连接是正常的，继续接收
        {
            continue;//继续接收数据
        }
        break;//跳出接收循环
    }
}
```

```
Linux环境下，须如下定义：
struct timeval timeout = {3,0}; 
//设置发送超时
    setsockopt(m_socket, SOL_SOCKET,  SO_SNDTIMEO,(const char *)&timeout,sizeof(struct timeval));

    //设置接收超时
    setsockopt(m_socket,SOL_SOCKET, SO_RCVTIMEO, (const char *)&timeout,sizeof(struct timeval));
```



recv等待对方的数据时，没有收到。

```
[11]:[Resource temporarily unavailable]
```

EAGAIN就是11 。



接收大量数据的时候，可以就在while循环里recv就好了。

只要缓冲器里有数据，recv就不会阻塞。

我从服务端一次发送2000字节，我接收的时候，一次收1023字节。

```
[DEBUG][TcpClient.cpp][connectToTcpServer][143]: recv n:1023
[DEBUG][TcpClient.cpp][connectToTcpServer][143]: recv n:977
```



有一个疑问，在recv的时候，怎么判断本次数据读取完成了呢？

就是返回-1的时候，且错误码是EAGAIN，就是recv数据完成了。

那么这里就涉及到一个超时时间的设置问题了。

我当前给3秒，太久了。多久合适呢？



recv一次处理多少数据是比较合适的呢？

默认的buf是这么大。我就按这个来了。这个80K左右，估计无论什么数据，一次都可以搞定了。

```
recv buf len:87380
send buf len:16384
```





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

2、socket网络编程中read与recv区别

https://my.oschina.net/lvsin/blog/383097