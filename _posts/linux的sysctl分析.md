---
title: linux的sysctl分析
date: 2016-12-12 18:52:53
tags:
	- linux 
	- sysctl
---
1

sysctl对应的是/proc/sys目录下。

sysctl是一个允许用户在运行时改变linux系统某些设置的接口，可以设置的变量个数超过500个。
查看当前的设置：`sysctl -a`
从得出的结果来看，这些设置项主要是net相关、vm相关、kernel相关、dev相关。net占据了很大一部分。
读取某个特定的设置，直接加上设置的名称：`sysctl vm.block_dump`
设置某个值，用-w参数：`sysctl -w vm.block_dump=1`
`/etc/sysctl.conf`是一个在开机时就进行配置的文件。里面的设置语法是`var=value`的格式。
value的取值可能是：字符串、数字、布尔值。（布尔值用0和1来表示）。
sysctl的功能和proc文件系统有交叉，一个功能的设置，既可以用syctl，也可以用写proc文件的方式来做。
syctl是proc的一个使用接口，最终都是改到proc文件系统里了。
例如常用的打开ip转发功能的设置。
用sysctl：`sysctl -w net.ipv4.ip_foward=1`
用proc：`echo 1>/proc/sys/net/ipv4/ip_foward`
如果想要开机就打开ip转发，那么在/etc/sysctl.conf里加上`net.ipv4.ip_foward=1`就好了。

下面看看这个功能在内核里的相关代码。
```
调用流程：
start_kernel --> 
	proc_root_init -->
		proc_sys_init-->
			sysctl_init 
```


