---
title: busybox里的网络相关命令代码分析
date: 2017-05-04 20:01:11
tags:

	- busybox

---

# 1. ifconfig

这个是分析的第一个命令，所以就分析全面一点，从ifconfig.c里包含的头文件开始分析。

## 1.1 头文件分析

* `<net/if.h>`

```
if.h
	<sys/types.h>
		定义基础数据类型，u_int_8_t这些。
	<sys/sockets.h>
		声明socket、accept等函数。
	定义结构体：
		struct ifaddr
		struct ifreq
		struct ifconf
		
```

在net目录下，一共有10个头文件。

* `<net/if_arp.h>`

```
if_arp.h
	定义结构体：
		struct arphdr
		struct aprreq
		
```

* `<netinet/in.h>`

```
in.h
	定义结构体
		struct in_addr
		struct sockaddr_in
		
```

netinet目录下，有13个头文件。

* <net/ethernet.h>

```
ethernet.h
	定义结构体：
		struct ether_addr
		struct ether_header
		
```

头文件主要就是上面这几个。

## 1.2 main函数

函数流程分析，用gdb来跟读流程：

```
main
	1. 如果检测到只有ifconfig
	2. 调用networking/interface.c里的display_interface来显示网卡信息。
		if_printf
			从/proc/net/dev目录下读取文件内容。
			任意打开一个socket:fd = socket(AF_INET, SOCK_DGRAM, 0)，对fd用ioctl查询信息。
			结合上面两个方面的信息，就得到了最后的内容。
	
```



# 2. route

## 2.1 头文件

* `<net/route.h>`

```
route.h
	结构体定义：
		struct rtentry
		
```

## 2.1 main函数

信息来源还是proc里。`/proc/net/route`。都是读取这个信息，再进行整理得到最终的结果。



