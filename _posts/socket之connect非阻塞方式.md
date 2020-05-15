---
title: socket之connect非阻塞方式
date: 2020-05-08 15:23:08
tags:
	- socket

---

1

我设置为非阻塞方式connect，直接就返回错误了。

调用connect连接一般的超时时间是75s, 但是在程序中我们一般不希望等这么长时间采取采取动作。

 可以在调用connect之前设置套接字非阻塞,然后调用connect,此时connect会立刻返回, 如果连接成功则直接返回0（成功）， 如果没有连接成功，也会立即返回并且会设置errno为EINPROCESS,这并不是一个致命错误,仅仅是告知你已经在连接了,你只要判断是它就继续执行后面的逻辑就行了,比如select.

通过select设置超时来达到为connect设定超时的目的. 

自己封装一下connect函数。用SO_SNDTIMEO来设置连接时间。

```
int timeout_connect(int sockfd, struct sockaddr *addr, int len, struct timeval *timeout)
{
    int ret = 0;
    socklen_t n = sizeof(*timeout);
    ret = setsockopt(sockfd, SOL_SOCKET, SO_SNDTIMEO, timeout, n);
    if(ret < 0) {
        myloge("set socket send timeout fail, reason:%s", strerror(errno));
        return -1;
    }
    ret = connect(sockfd, addr, len);
    if(ret < 0) {
        if(errno == EINPROGRESS) {
            myloge("connect timeout");
            return -1;
        }
        myloge("other connect error, reason:%s", strerror(errno));
        return -1;
    }
    return 0;
}
```



参考资料

1、

https://blog.csdn.net/abccheng/article/details/74216601

2、设置socket connect超时时间的几种方法

https://blog.csdn.net/xiongya8888/article/details/96996236