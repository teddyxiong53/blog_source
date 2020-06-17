---
title: socket之getaddrinfo函数
date: 2020-06-15 15:46:49
tags:
	- Linux

---

1

getaddrinfo是把gethostbyname和getservbyname这2个函数统一为一个函数了。

gethostbyname只支持ipv4，而且不支持调用的时候指定信息。

getaddrinfo是为ipv6加入的。

而且getaddrinfo是可以重入的。

这几个函数都是在netdb.h头文件里。

后面我自己统一只时延getaddrinfo这个函数。

```
原型：
	int getaddrinfo(const char *node, const char *service,
                       const struct addrinfo *hints,
                       struct addrinfo **res);
参数1：
	是一个字符串地址。例如ip地址，或者主机名。可以为NULL。还可以是ipv6地址。
参数2：
	服务字符串。可以是一个端口号的字符串。也可以是ftp、http这种名字。具体查看/etc/services 文件
	参数1和参数2，可以是NULL，但是不能同时都是NULL。
参数3：
	获取的要求。
	例如，可以指定ai_flags为AI_NUMERICHOST，这样就只解析ip地址，禁止解析域名。
	可以是NULL。
	一般用法是：定义一个栈上变量。然后memset为0 。
	只有4个成员可以被设置：ai_family、ai_socktype、ai_protocol、ai_flags。
	ai_family：AF_INET / AF_INET6 / AF_UNSPEC（这个表示IPV4和IPV6都可以）
	
参数4：
	输出结果到这里。
	
返回值：
	0表示成功。
	其他返回值表示错误。
	可以用gai_strerror(ret)来打印错误信息。
	
```

需要在同一个函数内部进行释放：

```
freeaddrinfo
```



getaddrinfo可以支持两种转换：

1、主机名到地址。

2、服务到端口号。





参考资料

1、man手册

2、getaddrinfo详解

https://www.cnblogs.com/fnlingnzb-learner/p/7542770.html

