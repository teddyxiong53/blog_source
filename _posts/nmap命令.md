---
title: nmap命令
date: 2020-03-04 09:33:28
tags:
	- 渗透

---

1

nmap现在可以用lua来写脚本，实际上也成为一个框架性的工具了。

nmap脚本引擎Nmap Script Engine，简称NSE。

目前nmap默认已经带了数百个扩展脚本了。

nmap的4个基本功能：

1、主机发现。

2、端口扫描。

3、服务检测。

4、os检测。

通过脚本扩展了这些能力：

1、http服务探测。

2、暴力破解简单密码。

3、检查漏洞信息。



实用命令：

检测所有alive的机器

```
sudo nmap -sn 192.168.0.0/24 
```



命令格式：

```
nmap [scan type] [opt] {target}
```

目标可以是：

```
hostname、ip、网络名。
```

主机发现相关选项：

```
-sL 
	这个表示只是把要扫描的目标列出来而已。不进行操作。
	举例：sudo nmap -sL 192.168.0.0/24
-sn
	相当于scan disable，不扫描端口，只进行ping操作。
	举例：sudo nmap -sn 192.168.0.0/24  这个比较有用。
-Pn
	这个是把网络里的所有机器都当成online处理。
	相当于ping disable。
	不ping，直接扫描端口，其实不太好。浪费时间。
```

端口扫描相关选项

```
-px-y
	指定端口范围，例如-p1-65535
	-p U:53,111,137,T:21-25,80,139,8080,S:9
-F
	快速扫描。
-r
	表示连续扫描，而不是随机扫描。
	
```

服务检测相关选项

```
-sV
	检测端口来看服务信息。
	举例：sudo nmap -sV 192.168.0.105
		例如我的树莓派上，跑的ssh是dropbear的，这个就可以把这个信息显示出来。
		
```

脚本扫描

```
--script=xx
	xx可以是vuln，可以取值的很多，就是一个脚本的名字。
```

os检测选项

```
-O
	使能os检测。
	
```

时间和性能选项

```
-T x
	x取值范围1到5，数字越大，速度越快。
	
```

防火墙和欺骗

```
--mtu x
	修改自己的mtu。
-S ipaddr
	伪装自己的ip
	
```

输出：

```
-v
	verbose模式。-vv更加详细。
```



其他选项

```
-6
	使能ipv6扫描。
-A
	使能os检测、版本检测、脚本扫描、traceroute。
	
```



# 脚本

脚本都在/usr/share/nmap/scripts目录下，后缀是nse的。lua写的。

负责处理鉴权证书的脚本，可以用来检测部分应用弱口令。

```
sudo nmap --script=auth 192.168.0.105
```

简单的暴力破解

```
sudo nmap --script=brute 192.168.0.105
```

默认的脚本扫描，主要是收集应用的各种信息。这个还可以有用。

```
sudo nmap --script=default 172.16.2.117
```



参考资料

1、一些Nmap NSE脚本推荐

http://www.polaris-lab.com/index.php/archives/390/

2、Nmap的高级扫描（脚本）

https://blog.csdn.net/u012206617/article/details/85283834