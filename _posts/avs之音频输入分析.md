---
title: avs之音频输入分析
date: 2018-11-10 14:59:19
tags:
	- avs
---



AudioProvider

AudioInputStream

SharedDataStream 这个是一个类模板。



executeRecognize这个函数是如何把输入音频上传到avs服务器的呢？

创建了一个reader。

```
m_reader = avsCommon::avs::attachment::InProcessAttachmentReader::create(
```

看这个read函数如何调用的。

```
std::size_t InProcessAttachmentReader::read(
```





SourceInterface

BaseStreamSource

