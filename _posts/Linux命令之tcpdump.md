---
title: Linux命令之tcpdump
date: 2017-08-08 22:54:52
tags:

	- Linux命令

---

1

tcpdump是一个抓包工具。抓包的时候，最好把网卡设置为混杂模式，这就需要root权限。

# 常用命令

普通情况下，直接启动tcpdump将监视第一个网络接口上所有流过的数据包。

```
tcpdump
```

抓包的结果，就直接在当前控制台打印出来。



基本选项：

```
-i wlan0：指定网卡，interface缩写。
src host 192.168.0.10 指定本机的哪个网卡。
dst host 114.114.114.114 指定目标主机。
src port 1234 本机端口
dst port 80  目标端口

可以使用and or not这些逻辑条件。
-w xx 结果写入到文件xx里。而不是打印在控制台。
```



抓mqtt包

```
tcpdump -AX -i wlan0   tcp port 39486 -w mqtt.cap
```

39486 这个是本地的端口号，对方的端口号是1883 。

可以写目的端口号，是这样：

```
tcpdump -AX -i wlan0   dst port 1883 -w mqtt.cap
```







 根据以上分析，可以通过改善tcpdump上层的处理效率来减少丢包率，下面的几步根据需要选用，每一步都能减少一定的丢包率
 1. 最小化抓取过滤范围，即通过指定网卡，端口，包流向，包大小减少包数量
 2. 添加-n参数，禁止反向域名解析
 3. 添加-B参数，加大OS capture buffer size
 4. 指定-s参数, 最好小于1000
 5. 将数据包输出到cap文件
 6. 用sysctl修改SO_REVBUF参数，增加libcap缓冲区长度:/proc/sys/net/core/rmem_default和/proc/sys/net/core/rmem_ma



参考资料

1、tcpdump 抓包工具使用

https://www.cnblogs.com/yorkyang/p/7654647.html

2、tcpdump丢包分析

https://blog.csdn.net/blade2001/article/details/41543297

3、tcpdump 很详细的

http://blog.chinaunix.net/uid-11242066-id-4084382.html