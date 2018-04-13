---
title: Linux之网络地址转换函数
date: 2018-04-13 19:11:11
tags:
	- Linux

---



经常需要把各种格式的网络地址相互转化，对应的函数梳理一下。

依赖的头文件是arpa/inet.h。

主要的函数有：

#字符串转u32

```
in_addr_t inet_addr(const char *);
输入：
	"127.0.0.1"这种字符串。
输出：
	in_addr_t，就是一个u32的。
```

```
in_addr_t inet_network(const char *)
输入：
	"127.0.0.1"这种字符串。
输出：
	in_addr_t，就是一个u32的。
可以看到inet_addr和inet_network的输入输出类型是一样的。
他们有什么区别？
inet_addr得到的是网络字节序的。
inet_network得到的是主机字节序的。
```

```
int inet_aton(char *, struct in_addr *)
输入：
	"127.0.0.1"这种字符串。
输出：
	struct in_addr。里面就是封装了一个in_addr_t的成员。得到的也是网络字节序的。
返回值：
	0：成功。
	1：失败。
```

# u32转字符串

```
char *inet_ntoa(struct in_addr)
输入：
	server_addr.sin_addr这样。
输出：
	"127.0.0.1"这种字符串。
实现：
char *inet_ntoa(struct in_addr in)
{
	static char buf[16];
	unsigned char *a = (void *)&in;
	snprintf(buf, sizeof buf, "%d.%d.%d.%d", a[0], a[1], a[2], a[3]);
	return buf;
}
```

我先看这4个，后续有需要再继续补充。



我优先使用inet_aton和inet_ntoa，因为看起来对称，而且是网络字节序。用法也是最自然的，输出在返回值里。



# 参考资料

1、inet_addr()、inet_network()、inet_aton()的区别

https://blog.csdn.net/nokiaxjw/article/details/8083843