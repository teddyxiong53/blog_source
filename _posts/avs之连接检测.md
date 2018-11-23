---
title: avs之连接检测
date: 2018-11-22 17:48:19
tags:
	- avs
---



这个是简单功能，但是用到了几个我不太熟悉的类，所以可以作为一个切入点，来分析用到的类。

主要是2个类：

1、HTTPContentFetcherInterfaceFactoryInterface。实现类是HTTPContentFetcherFactory。需要的参数，就是一个url。实际又是封装了LibCurlHttpContentFetcher（把url往下传递了）。这个类里最主要的方法getContent。

2、InProcessAttachment。

3、HTTPContent。这个很简单，没有函数。重要成员是InProcessAttachment> dataStream;



这样来获取文本内容：

```
auto httpContent = contentFetcher->getContent(HTTPContentFetcherInterface::FetchOptions::ENTIRE_BODY);
```



然后把数据读到一个buffer里，find里面有没有特定的字符串，有说明连接正常。



5分钟检查一次。

```
static const std::chrono::minutes DEFAULT_TEST_PERIOD{5};
```

