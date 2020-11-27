---
title: python之bs4学习
date: 2018-10-21 10:43:24
tags:
	- Python

---



现在需要爬一个简单的网页，用最基础的工具就可以了。

所以就用bs4来做。

学习一下基本用法。



如果一个正则匹配稍有差池，那可能程序就处在永久的循环之中，

而且有的小伙伴们也对写正则表达式的写法用得不熟练，

没关系，我们还有一个更强大的工具，叫 Beautiful Soup，

**有了它我们可以很方便地提取出 HTML 或 XML 标签中的内容，**

实在是方便，这一节就让我们一起来感受一下 Beautiful Soup 的强大吧。

简单来说，Beautiful Soup 是 python 的一个库，最主要的功能是从网页抓取数据。



Beautiful Soup 提供一些简单的、python 式的函数用来处理**导航、搜索、修改分析树**等功能。

它是一个工具箱，通过解析文档为用户提供需要抓取的数据，

因为简单，所以不需要多少代码就可以写出一个完整的应用程序。 

Beautiful Soup **自动将输入文档转换为 Unicode 编码，输出文档转换为 utf-8 编码。**

你不需要考虑编码方式，除非文档没有指定一个编码方式，这时，Beautiful Soup 就不能自动识别编码方式了。

然后，你仅仅需要说明一下原始编码方式就可以了。

 Beautiful Soup 已成为和 lxml、html6lib 一样出色的 python 解释器，

为用户灵活地提供不同的解析策略或强劲的速度。

Beautiful Soup 3 目前已经停止开发，推荐在现在的项目中使用 Beautiful Soup 4，不过它已经被移植到 BS4 了，也就是说导入时我们需要 import bs4 。



Beautiful Soup 将复杂 HTML 文档转换成一个复杂的树形结构，每个节点都是 Python 对象，所有对象可以归纳为 4 种:

- Tag
- NavigableString
- BeautifulSoup
- Comment

下面的代码，都已这个html文本作为测试对象。

```
from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
```



Tag 是什么？通俗点讲就是 HTML 中的一个个标签

HTML 标签加上里面包括的内容就是 Tag，下面我们来感受一下怎样用 Beautiful Soup 来方便地获取 Tags 下面每一段代码中注释部分即为运行结果

打印内容：

```
soup = BeautifulSoup(html, features='lxml')
print(soup.prettify())
```

获取title

```
print(soup.title)
```

得到：

```
<title>The Dormouse's story</title>
```

也可以获取p、a等标签。

这样的方式，只是获取第一个。

```
print(soup.p)
```

如果要查询所有的标签，我们在后面进行介绍

对于 Tag，它有两个重要的属性，是 name 和 attrs，下面我们分别来感受一下 **name**

```
print(soup.name)
print(soup.head.name)
```

得到：

```
[document]
head
```

soup 对象本身比较特殊，它的 name 即为 [document]，对于其他内部标签，输出的值便为标签本身的名称。 

下面看attrs

它是一个dict，把所有属性都组织起来。

```
print(soup.p.attrs)
```

得到：

```
{'class': ['title'], 'name': 'dromouse'}
```

既然得到的是dict，那么就可以用[]来进行使用每一个属性。

可以修改，也可以删除。

```
soup.p['class']='newClass'
```

```
del soup.p['class']
```

不过，对于修改删除的操作，不是我们的主要用途，

拿到标签里的文本内容：用string属性。

```
soup.p.string
```

它的类型是一个 NavigableString，翻译过来叫 可以遍历的字符串

BeautifulSoup 对象表示的是一个文档的全部内容。大部分时候，可以把它当作 Tag 对象，是一个特殊的 Tag，我们可以分别获取它的类型，名称，以及属性来感受一下

Comment 对象是一个特殊类型的 NavigableString 对象，其实输出的内容仍然不包括注释符号，但是如果不好好处理它，可能会对我们的文本处理造成意想不到的麻烦。 我们找一个带注释的标签

```
print(soup.a.string)
```

得到是是：

```
Elsie
```

本来是：

```
<!-- Elsie -->
```

这个就有点不对了。

我们需要判断一下soup.a的类型

```
print(type(soup.a.string))
```

得到：

```
<class 'bs4.element.Comment'>
```

```
if type(soup.a.string)==bs4.element.Comment:
    print(soup.a.string)
```



# 参考资料

1、使用BeautifulSoup解析HTML和XML

https://blog.csdn.net/bagboy_taobao_com/article/details/15505059

2、Python爬虫利器二之Beautiful Soup的用法

https://cuiqingcai.com/1319.html