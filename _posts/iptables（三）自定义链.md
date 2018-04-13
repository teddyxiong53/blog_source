---
title: iptables（三）自定义链
date: 2018-04-13 13:50:45
tags:
	- iptables

---



前面的操作，我们都是在默认的INPUT这个链上进行的，iptables运行我们创建自己的链。

```
iptables -t filter -N IN_WEB
```

这样，我们就创建了一个自己的名字叫IN_WEB的链。

```
vm-alpine-0:~# iptables -nvL IN_WEB
Chain IN_WEB (0 references)
 pkts bytes target     prot opt in     out     source               destination         
```

我们往这个链里面加一些规则。

```
iptables -t filter -I IN_WEB -s 192.168.190.137 -j REJECT
```

查看。

```
vm-alpine-0:~# iptables -nvL IN_WEB
Chain IN_WEB (0 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 REJECT     all  --  *      *       192.168.190.137      0.0.0.0/0            reject-with icmp-port-unreachable
```

给IN_WEB这个链改名字。

```
iptables -E IN_WEB WEB
```

清空这个链。

```
iptables -F WEB
```

删除这个链。

```
iptables -X WEB
```

