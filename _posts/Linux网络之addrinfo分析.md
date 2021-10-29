---
title: Linux网络之addrinfo分析
date: 2021-10-26 15:05:33
tags:
	- 网络

---

--

结构体是这样：

```
struct addrinfo
{
int ai_flags;
int ai_family; //AF_INET,AF_INET6,UNIX etc
int ai_socktype; //STREAM,DATAGRAM,RAW
int ai_protocol; //IPPROTO_IP, IPPROTO_IPV4, IPPROTO_IPV6 etc
size_t ai_addrlen;//length of ai_addr
char* ai_canonname; //full hostname
struct sockaddr* ai_addr; //addr of host
struct addrinfo* ai_next;
}
```

对应的函数是：

```
int getaddrinfo( const char *hostname, const char *service, const struct addrinfo *hints,
struct addrinfo **result );
hostname：主机名或者ip地址字符串。
service：服务的名字，或者10进制的字符串。
hints：可以是空指针。也可以是一个addrinfo结构体。用来指定某些信息，
	例如某个服务既支持tcp又支持udp，但是现在我就想要指定要udp的。
	那么把ai_socktype指定为SOCK_DGRAM就可以了。
```

这个函数可以实现2个转换：

1、主机名到地址的转换。

2、服务到端口的转换。

返回的结果是地址链表，具有协议无关性。



getaddrinfo的返回的内容的内存是动态分配的。需要后续调用freeaddrinfo来进行释放。



参考资料

1、

https://blog.csdn.net/wallwind/article/details/7787569