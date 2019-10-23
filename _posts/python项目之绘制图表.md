---
title: python项目之绘制图表
date: 2019-10-19 17:48:49
tags:
	- Python

---

1

这个是《python基础教程》（第三版）第21章内容的学习。



原书代码在这里：

https://github.com/teddyxiong53/beginning_python_source_code/tree/master/Chapter21

本章要做的是用python来绘制图表。

具体来说，是生成一个pdf文件，里面的图表是对下载的文本文件的数据进行了可视化。

PDF是Portable Document Format的意思。可以用来表示任何包含图形和文本的文档。

python很适合用来分析数据，尤其对于复杂逻辑。

本章用reportlib来绘制太阳黑子的折线图。

涉及的功能点：

```
1、从网上下载数据文件。
2、对数据文件进行解析，提取感兴趣的部分。
3、对数据生成图表。
```

选择reportlib是因为使用起来很简单，而且提供了丰富的pdf生成功能。

