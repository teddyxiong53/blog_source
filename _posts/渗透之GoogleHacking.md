---
title: 渗透之GoogleHacking
date: 2020-09-24 16:38:30
tags:
	- 渗透

---

1

谷歌黑客，也叫**Google dorking**，是一种利用谷歌搜索和其他谷歌应用程序来**发现网站配置**和计算机代码中的安全漏洞的计算机黑客技术。

利用谷歌搜索引擎中的高级操作符，在搜索结果中定位特定的文本字符串。 

一些比较流行的例子是找到易受攻击的 Web 应用程序的特定版本。

 带有 intitle: admbook intitle: Fversion filetype: php 的搜索查询将定位所有包含该特定文本的网页。

 应用程序的默认安装通常会在它们所服务的每个页面中包含它们的运行版本，例如，“由 XOOPS 2.2.3 Final 提供支持”。

设备连接到互联网上可以找到。 搜索字符串如 `inurl:"ViewerFrame?``Mode="` 将找到公开网络摄像头。

另一个有用的搜索是 intitle: index.of 后面跟着一个搜索关键字。 这可以给出服务器上的文件列表。 例如，intitle: index.of MP3将提供各种服务器上可用的所有 MP3文件。

“谷歌黑客”的概念可以追溯到2002年，当时Johnny Long开始收集谷歌的搜索查询，这些查询揭示了脆弱的系统和/或敏感信息的披露，并给它们贴上了googleDorks的标签。[[3\]](https://zh.wikipedia.org/wiki/谷歌黑客#cite_note-googleDorks2002-3)

Google Dorks列表发展成一个庞大的查询字典，最终在2004年被组织到原始的Google Hacking数据库（GHDB）中



参考资料

1、

https://zh.wikipedia.org/wiki/%E8%B0%B7%E6%AD%8C%E9%BB%91%E5%AE%A2