---
title: dns之python库分析
date: 2019-01-11 14:16:51
tags:
	- dns

---



dns库还文件还比较多，有几十个。

其中dns.resolver。ssr里应该是自己实现了类似这个的功能。

```
Help on module dns.resolver in dns:

NAME
    dns.resolver - DNS stub resolver.

FILE
    /usr/lib/python2.7/dist-packages/dns/resolver.py

DESCRIPTION
    @var default_resolver: The default resolver object
    @type default_resolver: dns.resolver.Resolver object

CLASSES
    __builtin__.object
        Answer
        Cache
        LRUCache
        LRUCacheNode
        Resolver
```





