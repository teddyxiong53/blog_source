---
title: Linux之mdns
date: 2020-03-12 14:49:13
tags:
	- buildroot

---

1

mdns，也是dns，就是域名解析服务器。

普通的dns服务器，就是我们常用的114.114.114.114这种。

是基于单播的。

而mdns，是基于组播的。

mdns可以和dns一起工作。

mdns基于udp。

最开始就是用来发现网络里的打印机的。

约定的组播地址是：224.0.0.251，端口号是5353



默认情况下，mdns只是用来解析以.local作为顶级域名的地址。

一个场景描述：

1、主机A进入到了局域网。A开启了mdns服务。并且向mdns注册了这样的信息：我提供了ftp服务，我的ip是192.168.1.101，我的ftp服务端口号是21 。

2、当主机B进入到局域网后，主机B的用户手动向自己的mdns服务提交请求：我要找局域网里的ftp服务器。然后B的mdns进程就在局域网里进行查询，最后得知192.168.1.101这个机器在21号端口提供了ftp服务。



参考资料

1、mdns 

https://baike.baidu.com/item/mdns/7544078?fr=aladdin

2、

https://blog.csdn.net/yueqian_scut/article/details/52694411?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task