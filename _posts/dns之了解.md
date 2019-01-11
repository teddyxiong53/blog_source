---
title: dns之了解
date: 2018-01-07 08:04:25
tags:
	- dns
	- 网站

---



# 1. dns简介

就是把域名翻译为ip地址的系统。

dns协议基于udp。端口号是53号。

在dns系统中，常见的资源记录类型有：

1、主机记录（A记录）

A记录的得名是Address记录的意思。

记录的表示含义类似这样：

```
www.xxx.com 转到11.11.11.11
mail.xxx.com 转到22.22.22.22
```

2、别名记录（CNAME记录）

CNAME记录用于把某个别名指向某个A记录上。这样就不需要再为某个新的名字增加一条新的A记录。

例如：

```
host.xxx.com 指向 11.11.11.11
www.xxx.com和mail.xxx.com都指向host.xxx.com

```

CNAME记录使用比A记录更加方便。推荐用CNAME记录。



3、MX记录（Mail Exchange）

邮件交换记录。这个不太理解。先不管。

4、NS记录（Name Server）

域名服务器记录。

5、ipv6记录。（AAAA记录）

# 2. 域名系统

全球有13台逻辑域名服务器。名字依次叫做A到M。

而物理上实际存在的根服务器在2014年统计为386台。分布于全球各地。

为什么逻辑上是13台呢？这个跟dns协议有关。dns协议使用了udp和tcp协议。udp协议用于查询和响应。tcp用于主服务器和从服务器之间的传递。

由于在udp查询和响应中，能保证正常工作的最大长度是512字节，512字节限制了根服务器的数量和名字，要让所有的根服务器数据可以包含在一个512字节的udp包里，根服务器的数量只能限制在13台。





相关的命令有：

```
host
dig：替代nslookup的。好用些。
nslookup

```

相关文件：

```

```



```
hlxiong@hlxiong-VirtualBox:~$ nslookup 127.0.0.1
Server:         127.0.0.1
Address:        127.0.0.1#53

1.0.0.127.in-addr.arpa  name = localhost.

hlxiong@hlxiong-VirtualBox:~$ nslookup 8.8.8.8
Server:         127.0.0.1
Address:        127.0.0.1#53

Non-authoritative answer:
8.8.8.8.in-addr.arpa    name = google-public-dns-a.google.com.

Authoritative answers can be found from:
```



用dig命令查看。

```
hlxiong@hlxiong-VirtualBox:~$ dig

; <<>> DiG 9.10.3-P4-Ubuntu <<>>
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 60294
;; flags: qr rd ra; QUERY: 1, ANSWER: 13, AUTHORITY: 0, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4000
;; QUESTION SECTION:
;.                              IN      NS

;; ANSWER SECTION:
.                       367839  IN      NS      f.root-servers.net.
.                       367839  IN      NS      k.root-servers.net.
.                       367839  IN      NS      b.root-servers.net.
.                       367839  IN      NS      l.root-servers.net.
.                       367839  IN      NS      e.root-servers.net.
.                       367839  IN      NS      a.root-servers.net.
.                       367839  IN      NS      d.root-servers.net.
.                       367839  IN      NS      h.root-servers.net.
.                       367839  IN      NS      m.root-servers.net.
.                       367839  IN      NS      c.root-servers.net.
.                       367839  IN      NS      i.root-servers.net.
.                       367839  IN      NS      g.root-servers.net.
.                       367839  IN      NS      j.root-servers.net.

;; ADDITIONAL SECTION:
d.root-servers.net.     604212  IN      AAAA    2001:500:2d::d
c.root-servers.net.     604513  IN      AAAA    2001:500:2::c

;; Query time: 8 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Fri Jan 11 11:11:51 CST 2019
;; MSG SIZE  rcvd: 295
```





域名系统也类似通讯录。大家记不住电话号码，就把电话号码跟名字对应起来。根据名字来查找。



参考资料

1、Linux 如何查看修改DNS配置

http://www.cnblogs.com/kerrycode/p/5407635.html

2、

http://www.jackxiang.com/post/7038/

3、DNS协议详解及报文格式分析

https://blog.csdn.net/tianxuhong/article/details/74922454