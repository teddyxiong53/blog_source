---
title: 网页之dom的element
date: 2019-04-19 13:31:25
tags:
	- 网页

---



在html的dom里，Element表示一个html元素。

我们翻译为元素。

属性和方法有：

```
accessKey：对应的快捷键。
appendChild()：向元素增加子节点。
attributes：返回NamedNodeMap。
childNodes：返回子节点的NodeList。
className：元素的class属性。
clientHeight：元素的高度。
clientWidth：元素的宽度。
cloneNode()：克隆元素。
compareDocumentPosition()：比较2个元素的文档位置。
contentEditable：是否可编辑。
dir：方向。
firstChild：第一个子节点。
getAttribute()：返回参数指定的属性。
getAttitbuteNode()：返回对应属性的节点。
getElementsByTagName()
getFeature()
getUserData()
hasAttribute()
hasAttributes()
hasChildNodes()
id
innerHTML
insertBefore()
isContentEditable
isDefaultNamespace()
isEqualNode()
isSameNode()
isSupported()
lang：元素的语言代码。
lastChild
namespaceURI
nextSibling
nodeName
nodeType
nodeValue
normalize()：合并元素中相邻的文本节点，并移除空格。
offsetHeight：元素的高度？跟clientHeight有什么关系？
offsetWidth
offsetLeft
offsetTop
owerDocument：返回文档对象。
parentNode
previousSibling
removeAttribute()
removeAttributeNode()
removeChild()
replaceChild()
scrollHeight：返回元素的整体高度。
scrollWidth
scrollTop
scrollLeft
setAttribute()
setAttributeNode()
setUserData()
style
tabIndex
tagName
textContent
title
toString()
item()
length
```

参考资料

1、HTML DOM Element 对象

http://www.w3school.com.cn/jsref/dom_obj_all.asp

