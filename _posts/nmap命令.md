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





一级扫描，先扫描有哪些端口开放了。

二级扫描，就针对某个端口，看看端口里的服务的漏洞。



nmap，扫描器之王。



在某些时候，我们大部分都使用Nmap进行扫描，

然后再通过Metasploit进行漏洞利用，

但是这个过程比较繁琐，

一个个漏洞去验证的话还需要打开MSF去设置参数，

最后run/exploit（不包括自动化，所以不要喷了）。

那么我们就要有必要认识一下Nmap的扩展脚本啦～

用这个命令，可以查看所有的脚本的名字。

```
ls /usr/share/nmap/scripts/ | sed 's/.nse//' > scripts.list
```

telnet暴力破解

```
nmap -p 23 --script telnet-brute --script-args userdb=myusers.lst,passdb=mypwds.lst,telnet-brute.timeout=8s <target>
```

-sC 这个选项表示--script=default。指定后，会调用一堆的脚本。没有什么事情，不用用这个。会很慢的。

https://nmap.org/nsedoc/categories/default.html

这个网页列出了default这个分类下的脚本。

脚本分类

```
auth
	负责绕开鉴权的脚本。
broadcast
	在局域网内探查更多服务开启的状况。例如dhcp、dns、sqlserver等服务。
brute	
	提供暴力破解。针对常见的http、snmp等。
default
	默认的脚本。
	主要是搜集各种应用服务的信息，收集到后，可再针对具体服务进行攻击
discovery
	对网络发现更多的信息，例如smb枚举，snmp查询。
dos
	进行ddos攻击。
exploit
	利用已知漏洞进行入侵。
external
	利用第三方的数据库或者资源，例如whois解析。
fuzzer
	模糊测试脚本。发送异常的包到目标机甲，探测出潜在的漏洞。
intrusive
	入侵性的脚本。可能会引发对方的IDS/IPS记录或者屏蔽。
	而且可能把目标机器搞挂掉。
malware
	探测目标机是否感染了病毒。
safe
	跟intrusive相反。属于安全性脚本。
version
	负责版本扫描。
vuln
	负责检查目标机是否有常见的漏洞。
	
```

这些分类脚本信息在/usr/share/nmap/scripts/scripts.db文件里。这个是一个文本文件。

里面内容是这样的：

```
Entry { filename = "x11-access.nse", categories = { "auth", "default", "safe", } }
Entry { filename = "xdmcp-discover.nse", categories = { "discovery", "safe", } }
Entry { filename = "xmlrpc-methods.nse", categories = { "default", "discovery", "safe", } }
Entry { filename = "xmpp-brute.nse", categories = { "brute", "intrusive", } }
Entry { filename = "xmpp-info.nse", categories = { "default", "discovery", "safe", "version", } }
```



不靠谱的脚本：

vnc-brute    次数多了会禁止连接

pcanywhere-brute   同上

/usr/share/nmap/nselib/data 这个目录下放了一些数据文件，简单的字典之类的。



不少人甚至认为它就是全球最好的扫描软件。除了常规的网络扫描，Nmap还可根据NSE (Nmap scripting Engine)的脚本进行大量渗透工作，这种脚本是基于Lua编程语言，有点像javascript。正是NSE，使得Nmap不再普通。

```
nmap site.test.lan --script http-enum
```

从上图中，我们可以了解到该站点使用了WordPress。于是，我们可以使用针对WordPress的脚本http-wordpress-enum进行深度扫描。这个脚本还会确定网站使用了多少和WordPress相关的插件。

```
nmap -p80 --script http-wordpress-enum --script-args http-wordpress-enum.search-limit=all site.test.lan
```

一般来说，标准的Nmap中集成了近600个脚本，如果没有你需要的，也可以自己编写脚本。

假如我们想在站点上寻找登录授权页面，还可使用如下脚本http-auth-finder。

```
nmap -p 8080 --script http-auth-finder 172.16.2.122
```



例如可以扫描出这个授权页面。

```
|   http://172.16.2.122:8000/c_mpermit  HTTP: Basic
|_  http://172.16.2.122:8000/c_options  HTTP: Basic
```



对于WordPress来说，Nmap已做的足够出色，它获取了大量和渗透有关的信息，而如果想对WordPress进行更深一步的漏洞探测，你也可以使用已集成在kali linux中的WPScan，这款软件有大量专门针对WordPress的PoC。

```
nmap --script exploit,malware 172.16.2.117
```

这个是比较有用的一条命令。

可以找到漏洞。然后在msfconsole里search一下。再利用看看。

不过很多时候是不成功。

```
[*] Exploit completed, but no session was created.
```

## 脚本使用高级

```
# 使用除了exploit之外的所有脚本
nmap --script "not exploit" xx
# 使用除了intrusive、dos之外的所有脚本。
nmap --script "not (instrusive or dos)" xx
# 只使用safe和voln
nmap --script "safe and vuln" xx
# 还支持通配符
nmap --script "snmp-*" xx
# 通配符和运算符结合
nmap --script "ftp-* and not (instrusive)" xx

```

```
# 传递参数给脚本
# 这样可以避免被当成爬虫屏蔽。
nmap -p 80 --script http-methods --script-args http.agent="Mozilla 50" www.baidu.com
```

```
#调试脚本
# 这样会把所有的数据都打印出来。其实太多了。
nmap -p 80 --script-trace --script http-methods www.baidu.com
# 还可以指定打印的级别从d1到d9。数字越大，打印越多。
nmap -p 80 -d1 --script-trace --script http-methods www.baidu.com
```

## 脚本常见应用

发现局域网里所有的活跃主机

```
nmap --script broadcast-ping 172.16.2.0/23
```

## 脚本规则

脚本后缀是nse，其执行也是调用了lua内部的解释器。

nse引擎的执行流程中首先会执行nse_main.lua脚本，该脚本做了以下事情

- 加载一些Nmap的核心库（nselib文件夹中）
- 定义多线程函数
- 定义输出结果处理函数
- 读取、加载扩展脚本
- 定义扩展脚本函数接口
- 执行扩展脚本

nse_main.lua脚本中规定了nmap脚本的执行顺序：各种rule规则和action动作。编写nse脚本也就是主要写rule函数和action，rule函数返回true时执行action函数。

**rule规则**

- prerule：扫描任何主机前执行一次
- hostrule：扫描一个主机后执行一次，多个主机执行多次
- portrule：扫描一个主机的端口后执行一次，多个主机执行多次
- postrule：全部扫描完毕后执行一次

我们都知道nmap自带了数百种脚本，自然也有其自定义的库函数，使用这些库函数可以方便我们模仿着已有的nse脚本写出能达到自己目的的脚本。

这里列出了nse的api。

https://nmap.org/book/nse-api.html

非官方的脚本，这里有：

https://github.com/cldrn/nmap-nse-scripts



知道nmap自带的脚本使用方法之后能更加准确的去收集信息，方便后续的渗透，

常规渗透思路应该是：扫端口，扫版本，扫漏洞，针对漏洞扫exp，

尽量不要一上来就用default脚本，那会降低扫描速度。



查看本机的网卡和路由信息

```
nmap --iflist
```

指定多个伪装ip，D表示Decoy（欺骗）,ME代表自己的ip地址

```
nmap -D 192.168.0.1,192.168.0.100,ME
```

定制扫描包的格式，就是指定tcp的flags

```
nmap --scanflags SYNFIN 
```

--ip-options则是指定ip报文的flags。



防火墙在今天网络安全中扮演着重要的角色，如果能对防火墙系统进行详细的探测，那么绕开防火墙或渗透防火墙就更加容易。所以，此处讲解利用Nmap获取防火墙基本信息典型的用法。

为了获取防火墙全面的信息，需尽可能多地结合不同扫描方式来探测其状态。在设计命令行参数时，可以综合网络环境来微调时序参数，以便加快扫描速度。

用syn包扫描

```
nmap -sS xx
```

用fin包扫描。FIN扫描方式用于识别端口是否关闭，收到RST回复说明该端口关闭，否则说明是open或filtered状态。

```
nmap -sF xx
```

用ack包扫描

```
nmap -sA xx
```

扫描路由器

Nmap内部维护了一份系统与设备的数据库（nmap-os-db），能够识别数千种不同系统与设备。所以，可以用来扫描主流的路由器设备。

扫描互联网上的web服务器

```
nmap -iR 100 -sS -PS80 -p 80 -oG result.txt
```



参考资料

1、一些Nmap NSE脚本推荐

http://www.polaris-lab.com/index.php/archives/390/

2、Nmap的高级扫描（脚本）

https://blog.csdn.net/u012206617/article/details/85283834

3、

https://wooyun.js.org/drops/nmap%E8%84%9A%E6%9C%AC%E4%BD%BF%E7%94%A8%E6%80%BB%E7%BB%93.html

4、

https://blog.51cto.com/14309999/2448178

5、nmap脚本

https://mntn0x.github.io/2019/08/02/nmap%E8%84%9A%E6%9C%AC/

6、nmap脚本使用总结

https://www.cnblogs.com/h4ck0ne/p/5154683.html

7、

https://zhuanlan.zhihu.com/p/40681245