---
title: Linux命令之netstat
date: 2017-08-07 21:06:22
tags:

	- Linux命令

---

netstat命令有五大作用：

1、显示网络连接信息。

2、显示路由信息。

3、显示接口统计信息。

4、显示无效连接信息。

5、显示组播成员信息。



netstat的输出内容分为两大部分，前面是tcp连接，后面是unix域socket。

# 1. 基础常用命令

1、`netstat -a`。列出所有的连接。

2、`netstat -at`。列出所有的tcp连接。

3、`netstat -au`。列出所有的udp连接。

4、`netstat -l`。列出所有的处于listen状态的端口。

5、`netstat -s`。统计所有的协议的情况。

6、`netstat -n`。表示不要把数字用字符串替代，这样看到的可能会更加清晰。

7、`netstat -c`。连续输出。

8、`netstat -r`。输出路由信息。等价于route命令。

9、`netstat -i`。按接口显示。

# 2. 复杂组合

