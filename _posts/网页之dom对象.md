---
title: 网页之dom对象
date: 2019-01-21 13:16:12
tags:
	- 网页

---



dom对象有：

```
document
element
attribute
event
```



# document

每个载入到浏览器的html文档都对应一个document对象。

document让我们可以对html文档里的每个元素进行操作。

document是window对象的一部分。

属性：

```
title
URL
...
```

方法：

```
open：返回一个stream。
close
write
writeln：写一个换行符。
getElementById/ByName/ByTagName。
```



# element

中文叫做节点。

html dom里，每个部分都是节点。

```
1、文档本身是节点。
2、所有的html元素是节点。
3、所有的属性是节点。
4、注释是注释节点。
```



参考资料

1、

http://www.w3school.com.cn/jsref/dom_obj_document.asp

2、这个网站更详细些。

https://www.w3cschool.cn/jsref/dom-obj-document.html