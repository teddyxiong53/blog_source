---
title: django之haystack
date: 2020-12-02 11:38:30
tags:
	- django
---



搜索是一个日益重要的话题。

用户越来越依赖于搜索从噪声信息中分离和快速找到有用信息。

此外，搜索搜索可以洞察那些东西是受欢迎的，改善网站上难以查找的东西。

为此，Haystack试图整合自定义搜索，

使其尽可能简单的灵活和强大到足以处理更高级的用例。

haystack支持多种搜索引擎，不仅仅是whoosh，使用solr、elastic search等搜索，

也可通过haystack，而且直接切换引擎即可，甚至无需修改搜索代码。



```
pip install django-haystack
pip install whoosh
pip install jieba
```

# whoosh

纯Python的全文搜索库，

Whoosh是索引文本及搜索文本的类和函数库。

它能让你开发出一个个性化的经典搜索引擎。

Whoosh 自带的是英文分词，对中文分词支持不太好，**使用 jieba 替换 whoosh 的分词组件。**





参考资料

1、Haystack的介绍和使用 

https://www.cnblogs.com/ay742936292/p/11165876.html

2、Whoosh模块

https://blog.csdn.net/qq_1290259791/article/details/84104799