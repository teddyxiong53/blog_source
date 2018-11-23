---
title: avs之attachment
date: 2018-11-21 10:42:19
tags:
	- avs
---



Attachment这个概念在avs系统里用到很多。我把层次关系梳理一下。

Attachment：基础类，主要函数都没有实现。可以当这个不存在。

InProcessAttachment：继承了Attachment。override了createReader和createWriter函数。这个是主要基础类。

AttachmentWriter

AttachmentReader

AttachmentManager



AttachmentWriter：主要就是一个write方法。

InProcessAttachmentWriter



AttachmentManager里，创建了InProcessAttachment

```
details.attachment = make_unique<InProcessAttachment>(attachmentId);
```

实际上是调用到



HTTPContentFetcherFactory这个主要是用来展开分析PlayList的。



attachment一个简单的应用是连接检查的那个类，是从一个url上下载一个文本文件，然后分析内容。

```
std::shared_ptr<avsCommon::avs::attachment::InProcessAttachment> m_stream;
```

构造这个attachment，参数就是一个url。

