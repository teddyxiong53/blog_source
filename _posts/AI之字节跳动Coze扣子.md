---
title: AI之字节跳动Coze扣子
date: 2024-05-10 10:34:11
tags:
	- AI
---

--

昨天看B站视频林Yi讲到了Coze这个AI平台。

感觉不错，可以自己进行工作流的配置调优。

这个目前在其他主流的平台好像没有看到。

值得研究一下。

# 海报工作流研究

https://www.coze.cn/store/imageflow/7407286107886518272?from=bots_card

这个工作流的构成：

一个输入节点，里面有这个输入项：

* image提示词。string类型。
* 主标题。string类型。
* 副标题。string类型。
* logo。image类型。
* ewm。image类型。这个是二维码。
* product。image类型。

输入节点的输出，流向了3个节点：

* 抠图节点。对logo进行抠图。
* 抠图节点1。这个是对product进行抠图。
* 图像生成。这个生成背景图片。

上面3个节点的输入，统一流向了一个节点，这个节点是画板。

画板节点：

* 拿到开始节点和3个图像节点的输入内容。
* 自己有一个画板的布局设置。
* 有一个输出预览。

画板节点连接到结束节点。

结束节点：

* 拿到画板节点的data。进行输入。



# 把网页总结为思维导图的教程

https://www.53ai.com/news/coze/2024080613286.html

https://www.53ai.com/news/qianyanjishu/2024060851347.html
