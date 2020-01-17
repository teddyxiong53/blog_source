---
title: gstreamer之appsrc
date: 2020-01-15 11:39:19
tags:
	- gstreamer
---

1

什么是appsrc？作用是什么？主要在什么情况下使用？

gstreamer网站上是这么写的。

The appsrc element can be used by applications to **insert data into a GStreamer pipeline**

是用来插入数据到pipeline的。

appsrc属于base plugin。在libgstapp.so里面。

既然名字里有src，那么这个就只有src pad。

src pad的特点是：任意类型，static的。

主要的特点是各种signals。

```
end-of-stream
enough-data
need-data
push-buffer
push-buffer-list
push-sample
seek-data
```

在什么情况下使用？

数据源没有对应的gstreamer插件的时候。

appsrc和appsink是应用程序跟pipeline进行交互的最简单的方式。

应用程序负责数据的生成，把数据作为GstBuffer传输到pipeline里。

appsrc通过监听enough-data和need-data来控制数据的发送。



gstreamer在各个plugin之间传递数据的数据块叫做buffer。

对应数据结构GstBuffer。

GstBuffer由srcpad产生，由sinkpad消费。

首先使用appsrc替代audiotestsrc用于产生audio数据，另外增加一个新的分支，将tee产生的数据发送到应用程序，由应用程序决定如何处理收到的数据。

为了避免混淆，我们可以这么来理解，appsrc是一个普通的source element，不过它的数据都是来自外太空，而appsink是一个普通的sink element，数据从这里出去的就消失不见了。



参考资料

1、

https://gstreamer.freedesktop.org/documentation/app/appsrc.html?gi-language=c

2、GStreamer基础教程09 - Appsrc及Appsink

https://www.cnblogs.com/xleng/p/11611450.html