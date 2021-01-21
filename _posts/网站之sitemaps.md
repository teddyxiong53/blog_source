---
title: 网站之sitemaps
date: 2021-01-19 09:47:11
tags:
	- 网站

---

--

Sitemap 可方便管理员**通知搜索引擎**他们网站上有**哪些可供抓取**的网页。

最简单的 Sitepmap 形式，就是 XML 文件，

在其中**列出网站中的网址以及关于每个网址的其他元数据**（上次更新的时间、更改的频率以及相对于网站上其他网址的重要程度为何等），以便搜索引擎可以更加智能地抓取网站。

网络抓取工具通常会通过网站内部和其他网站上的链接查找网页。

Sitemap 会提供此数据以便允许支持 Sitemap 的抓取工具抓取 Sitemap 提供的所有网址，

并了解使用相关元数据的网址。

使用 Sitemap [协议](https://www.sitemaps.org/zh_CN/protocol.html)**并不能保证网页会包含在搜索引擎中**，

但可向网络抓取工具提供一些提示以便它们更有效地抓取网站。



Google、雅虎、和微软都支持一个被称为xml网站地图（xml Sitemaps）的协议，

而百度Sitemap是指百度支持的收录标准，

在原有协议上做出了扩展。

百度sitemap的作用是通过Sitemap告诉百度蜘蛛全面的站点链接，优化自己的网站。

百度Sitemap分为三种格式：txt文本格式、xml格式、Sitemap索引格式。



文件协议应用了简单的XML格式，一共用到6个标签，

其中关键标签包括链接地址、更新时间、更新频率和索引优先权。



参考资料

1、官网

https://www.sitemaps.org/zh_CN/

2、百科

https://baike.baidu.com/item/sitemap/6241567?fr=aladdin