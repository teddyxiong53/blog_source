---
title: scrapy（2）
date: 2018-07-01 12:46:34
tags:
	- 爬虫

---



现在我们看看如何抓取真实的网站，我以抓网站图片为例。

scrapy爬取图片，需要用到ImagePipelilne这个类。这个类提供了一种方便的方式用来下载和存储图片。

这个类的主要功能有：

```
1、把下载图片转成通用的jpg和rgb文件格式。
2、避免重复下载。
3、可以生成缩略图。
4、图片大小可以实现自动过滤。
```

创建工程douban_img。



# 参考资料

1、

https://blog.csdn.net/Wilson_Iceman/article/details/79200796