---
title: 网络之socket函数分析
date: 2017-11-02 22:00:07
tags:
	- 网络

---



网络中进程通信首先要解决的问题是如何唯一标识一个进程。

本地是通过pid来唯一标识的。但是pid不能用在网络中来唯一识别一个进程。

那用什么？

其实tcpip协议栈已经帮我们解决了这个问题。网络层的ip地址可以唯一标识一台主机，而传输层的“协议+端口”可以唯一标识一个进程。

这样我们利用（IP地址，协议，端口）就可以标识网络中的进程了。



# 共用部分

1、socket函数。

```
3个参数：
1、domain。协议域。AF_INET（说明要用32位的ip地址和16位的端口号）。AF_INET6。AF_UNIX（说明要用绝对路径来做地址）。
2、type。socket类型。SOCK_DGRAM，SOCK_STREAM，SOCK_RAW。
3、protocol。协议。IPPROTO_TCP/IPPROTO_UDP。为0表示自动选择。我们一般给0 。
```

socket函数返回的是socket描述符存在于协议族空间里，没有ip地址信息。所以需要用bind函数给它赋一个地址。不然在connect或者listen的时候，会随机选择一个端口的。



# 服务端

1、bind函数。

```
3个参数：
1、int sockfd。
2、struct sockaddr *addr。这个是一个通用指针。我们实际会把sockaddr_in、sockaddr_in6、sockaddr_un传递过去。
3、socklen_t len。
```

客户端不用bind。因为我们就是希望客户端的端口随机生成。



2、listen函数。

```
2个参数。
1、int sockfd。
2、int backlog。可以排队连接到这个sockfd的最大排队数目。
```

listen函数使得一个socket从主动变为被动。

backlog是指处理多个连接时，可以让多少个进行排队。



在listen和accept之间，可以加上select来阻塞。但是accept其实也是阻塞的。

3、accept函数。**注意第三个长度参数，是一个指针。**

```
3个参数。
1、int sockfd。
2、struct sockaddr *addr。得到连接的client的地址。
3、socklen_t len。注意注意注意。这个是一个指针*len。如果给了一个值，就会出现accept的时候，Bad Address错误了。
```

输入的是前面listen的那个sock（叫监听socket）。得到的是另外一个sock值（叫连接socket）。这个sock表示的是跟client的tcp连接信息。

后续的recv和send都是用得到的连接sock来进行的。

监听socket在服务器进程的生命周期里都存在的。而连接socket在客户端端口后就不存在了。



4、收发函数。

read/write

recv/send

readv/writev

recvmsg/sendmsg

recvfrom/sento。

推荐使用recvmsg/sendmsg。是最通用的。不过我看lwip里没有实现这个接口。

格式是：

```
ssize_t recvmsg(int sockfd, struct msghdr *msg, int flags);
ssize_t sendmsg(int sockfd, const struct msghdr *msg, int flags);
```

核心就是struct msghdr。

```

```

5、close函数。

```
1个参数。
1、sockfd。
```



# fd_set分析

以lwip里的为例。

最多4个连接，FD_SETSIZE是4 。

得到定义的struct fd_set实际是：

```
struct fd_set {
  unsigned char fd_bits[1];
}
```

FD_SET就是把fd_bits里的对应的bit置位为1 。

假设第一个listenfd是3（0/1/2给了输入输出）。accept到的第一个connfd是4 。

定义一个int client[4]。用来存放connfd。里面内容初始化为-1 。

accept到一个连接后，把对应的connfd存放到client[]里。

发现connfd放满了，就提示连接太多了。

如果connfd大于maxfd，把connfd赋值给maxfd。

while（1）的处理分为2个部分，前半部分是处理连接，后半部分的处理收发。一个select就同时管到了listenfd和connfd。

然后是遍历client[]里的connfd。只要检查FD_ISSET(connfd)就好了。如果置位了，就进行read，read出错，就把connfd关闭，对应的FD_CLR掉，对应的client[]置位-1 。

read不出错，就进行write，给客户端回复。





