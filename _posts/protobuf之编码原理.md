---
title: protobuf之编码原理
date: 2019-11-27 14:43:06
tags:
	- 网络
---



1

Base 128 Varints的编码技术

 varints是一个使用一个或多个字节序列化整数的方法。数字越小，需要的字节数越少。

varint中的每个字节（最后一个字节除外）都设置了最高有效位（设置了最高位为1，否则为0），表示还有跟多的字节跟在后面。下文我们就称之为术语 msb 了。



参考资料

1、protobuf 编码原理

https://www.jianshu.com/p/814a5dd86561?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation