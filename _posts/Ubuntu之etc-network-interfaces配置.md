---
title: Ubuntu之etc-network-interfaces配置
date: 2021-06-04 10:47:11
tags:
	- 网络

---

--

大部分的网络接口配置都可以在/etc/network/interfaces中解决。

例如为网卡配置静态IP（dhcp），设置路由信息，配置IP掩码，设置默认路由等。

auto eth0

auto加网卡名，表示开机时就启动这个网卡。

然后就是配置网卡的ip地址，有两种：一种dhcp。一种static。

```
iface eth0 inet dhcp
iface eth0 inet static
	address 192.168.1.2
	netmask 255.255.255.0
	gateway 192.168.1.1
```

还有一个特别的loopback。

```
iface lo inet loopback
```



ifup -a 这个是如何处理interfaces这个文件的？

ifup和ifdown是对应了同一分代码，busybox/networking/ifupdown.c。

作用也非常简单，用法也简单，就是打开某个网卡，关闭某个网卡的语意。

本质还是使用了ifconfig、route、ip这些命令。

还有一个状态文件：/var/run/ifstate

内容是这样：

```
wlan0=wlan0
```

分析ifup的main函数

```
main
	const char *interfaces = "/etc/network/interfaces";
	read_interfaces(interfaces, NULL);
		这个注释里写了，只有以#开始的行才被当成注释，行尾的#不会被当成注释。
		解析文件内容，填充到结构体里。
		
```

iface_up函数

```
static int iface_up(struct interface_defn_t *iface)
{
	if (!iface->method->up(iface, check)) return -1;
	set_environ(iface, "start", "pre-up");
	if (!execute_all(iface, "pre-up")) return 0;
	if (!iface->method->up(iface, doit)) return 0;
	set_environ(iface, "start", "post-up");
	if (!execute_all(iface, "up")) return 0;
	return 1;
}

```



参考资料

1、

https://blog.csdn.net/m15511023218/article/details/87920263

2、Linux /etc/network/interfaces配置接口方法

https://www.jb51.net/article/180111.htm