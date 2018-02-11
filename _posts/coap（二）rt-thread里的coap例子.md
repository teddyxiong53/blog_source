---
title: coap（二）rt-thread里的coap例子
date: 2018-02-10 16:34:37
tags:
	- coap
	- rt-thread

---



rt-thread里集成了coap组件，并且提供了2个例子，一个coap client，一个coap server。我们先看client。

# client

有提供msh命令行工具。

用法是这样的：

```
msh />coap_client -m get coap://coap.me/test
uri.path.s = test; uri.host.s = coap.me/test 
server_host = coap.me
DNS lookup succeeded. IP=134.102.218.18
welcome to the ETSI plugtest! last change: 2018-01-15 13:55:19 UTC
```

http://coap.me/

这个网站是一个公共的测试网站。你可以向它查询coap信息。





