---
title: linux的iptables使用
date: 2016-12-02 22:07:33
tags:
	- linux
	- iptables
---
iptables是linux下的应用层防火墙工具。其实质是一个定义规则的配置工具，实际上工作的核心是Netfilter。
Netfilter是linux内核里的一个数据包处理模块。它的工作原理是往内核的协议栈里添加回调函数。
数据流在协议栈里流动时，一定会经过5个关键节点：`pre_routing、input、output、forward、post_routing`。
所以iptables的规则组成，就需要围绕这些节点来做文章。总结起来是一句话：四张表加五个点。
四张表是：
* filter表。用于过滤。
* nat表。用于地址转换。
* mangle表。用于修改数据表。
* raw表。用于处理异常。
五个点就是上面的五个关键节点。



# 1. 先查看当前已有的规则。
```
root@raspberrypi:/mnt# iptables -L -n
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
root@raspberrypi:/mnt# 
```
当前的input、output、forward规则都是空的。因为当前的系统默认选择了没有防火墙。

# 2. 增加一条规则
增加可以用`-A`和`-I`参数，A表示append，添加到末尾，I表示insert，可以插入到指定位置。
```
iptables -A INPUT -s 192.168.1.250 -j DROP

root@raspberrypi:/mnt# iptables -L -n
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
DROP       all  --  192.168.1.250        0.0.0.0/0           

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
```
