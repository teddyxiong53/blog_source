---
title: nodejs之tcp数据封装和解析
date: 2019-06-21 13:42:37
tags:
	- nodejs
---

1

现在要搭建一个简单的nodejs服务器，进行一个协议解析。

是在tcp上传输protobuf，前面还加了一个自定义的包头。

所以只能自己手动解析。回复也要加上包头。

tcp的nagle算法，会导致粘包和半包问题。

导致难以判断消息边界。





# 粘包问题解决

既然消息没有边界，我们可以在tcp传输的内容里添加边界。

一般有这些做法。

1、每次发送固定长度。不够灵活。

2、使用特殊标记来做边界。有风险。可能数据跟标记冲突。

3、把包的长度也放进去。需要增加对包头的解析。但是相对是比较好的。



目前我用的就是第三种的。



# 具体的代码实现





JavaScript处理二进制数据的方式

随着web应用的发展，现在经常需要使用js来处理音频、视频数据，或者通过WebSocket获取原始数据。

以前的js对于二进制数据的处理支持非常差。

所以现在新提出了TypedArray来进行二进制处理。

TypedArray分为2部分：

1、Buffer。缓冲区。

2、View。视图。

这样划分，是为了灵活同时保持高效率。

缓冲区由ArrayBuffer实现，一个缓冲区就是一块数据。没有格式，没有提供机制来进行访问。

要访问缓冲区的内容，你需要创建一个视图来做这个事情。

视图的基类的ArrayBufferView。这个类有一些子类。

例如Int8Array、Uint8Array。Float32Array。这样。

```
var buffer = new ArrayBuffer(16);
var view1 = new Int8Array(buffer);//基于buffer创建一个view。然后用来view才能进行读写。
view1[0] = 11//通过索引下标来做。
console.log(view1)
var view2 = new Int16Array(buffer)
console.log(view2[0])//得到的是0x3412 ，说明我的机器是小端的。
```





参考资料

1、基于Nodejs的Tcp封包和解包的理解

https://www.jb51.net/article/147661.htm

2、JavaScript处理二进制数据：TypedArrays

https://www.cnblogs.com/iicx/p/3859969.html