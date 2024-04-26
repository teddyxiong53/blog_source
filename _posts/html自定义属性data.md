---
title: html自定义属性data
date: 2020-12-31 11:23:11
tags:
	- html

---

1

data-* 全局属性 是一类被称为**自定义数据属性**的属性，

它赋予我们在所有 HTML 元素上嵌入自定义数据属性的能力，

并可以**通过脚本**在 HTML 与 DOM 表现之间**进行专有数据的交换。**



除了`data-`前缀之外，有效的自定义数据属性的名称必须只能包含字母、数字、连字符（ - ）、点（。）、冒号（:）或下划线（_），**不能包含大写字母。**



HTML5引入了data属性，它允许您在HTML元素中存储自定义数据。这些数据可以通过JavaScript访问，而无需使用非标准的属性。data属性是以"data-"开头的自定义属性。

例如，您可以这样在HTML元素中定义data属性：

```html
<div id="myElement" data-user-id="123" data-user-name="john_doe"></div>
```

在这个例子中，div元素有两个data属性：data-user-id和data-user-name。值可以是任何有效的字符串。

要通过JavaScript访问这些数据，您可以使用dataset属性。dataset属性提供了一个DOMStringMap对象，其中包含以data-为前缀的属性的键值对。

例如，您可以这样访问这个div元素的data属性：

```javascript
var element = document.getElementById("myElement");
var userId = element.dataset.userId; // 获取用户ID
var userName = element.dataset.userName; // 获取用户名
```

通过这种方式，您可以方便地将自定义数据存储在HTML元素中，并在JavaScript中轻松地访问它们。

# data属性在js代码里的名字不一样，是怎么对应起来的

在JavaScript中，通过dataset属性可以访问HTML元素上的data属性。dataset属性返回一个DOMStringMap对象，其中包含了以data-为前缀的属性名和对应的值。在JavaScript中，属性名会自动转换为驼峰式命名规则，去掉"data-"前缀，并将后续单词的首字母大写。

举个例子，假设有这样一个HTML元素：

```html
<div id="myElement" data-user-id="123" data-user-name="john_doe"></div>
```

在JavaScript中，您可以这样访问这个元素的data属性：

```javascript
var element = document.getElementById("myElement");
var userId = element.dataset.userId; // 获取用户ID
var userName = element.dataset.userName; // 获取用户名
```

在这里，"data-user-id"对应的JavaScript属性名为"userId"，"data-user-name"对应的JavaScript属性名为"userName"。这种自动转换使得访问data属性变得更加方便，无需手动处理属性名的格式。

# 参考资料

1、data-*

https://developer.mozilla.org/zh-CN/docs/Web/HTML/Global_attributes/data-*

2、

https://segmentfault.com/a/1190000009227732