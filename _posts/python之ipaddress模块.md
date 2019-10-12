---
title: python之ipaddress模块
date: 2019-10-08 16:10:22
tags:		
	- python

---

1

罗列出一个网段里所有的ip地址

```
net = ipaddress.ip_network("192.168.56.0/24")
for ip in net:
	print(ip)
	
注意，必须是192.168.56.0，注意最后这个0 。如果写成其他数字，则错误。
因为结尾0为0，才代表网络。
但是这个可以通过另外一个参数来解决。
就是strict=False，这样就可以任意写一个ip地址。
```



ping一个255个地址的网络，耗时500s左右。大概8分钟。非常久。

我用20个线程来做。

用10个线程来做，时间就缩短到50s左右，的确是提高了10倍。

用50个线程，只需要13秒左右。

用75个线程，10秒左右。

200个线程，需要9秒。

100个线程。也是9秒左右。

所以75个线程差不多了。



现在扫描所有ip都可以了。

接下来就是进行http请求machine_name。



参考资料

1、Python"ipaddress" 模块之概述

https://blog.csdn.net/j2iayu7y/article/details/80213273