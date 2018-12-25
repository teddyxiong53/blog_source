---
title: jQuery（一）
date: 2018-05-24 22:27:05
tags:
	- js

---



工作中涉及到一点jQuery，所以现在学习一下。

jQuery是一个js库。用来简化js编程的。

jQuery很容易学习的。



jQuery可以做什么？

1、html元素选取和操作。

2、css操作。

3、html事件函数。

4、js特效和动画。

5、html dom遍历和修改。

6、ajax。

7、utilities。



# 怎样安装

要在你的网页里加入jQuery，有两种方式：

1、在你的网站里放一份jQuery代码。

2、引用公共网址上的jQuery。

jQuery分为两种版本：

1、生产环境版本。被压缩过，体积小。不适合阅读。

2、测试环境版本。格式比较好，方便阅读和调试。



下载网站在这里。

https://code.jquery.com/jquery-3.3.1.js

我们把这个文件保存到本地就好了。

代码有1万行。



# 基本测试代码

下面的测试都在这个基础上改。

```
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>test</title>
    <script src="./jquery-3.3.1.js">

    </script>
    <script>
        $(document).ready(function() {
            //add your code here
            alert("hello jquery")
        })
    </script>

</head>
<body>

</body>
</html>
```

目录结构：

```
D:\work\test\jquery
λ  tree
.
├── jquery-3.3.1.js
└── test.html
```



# jQuery语法

本来$美元符在js语法里是没有特别意义的。

但是jQuery大量使用了，而且赋予了特别含义。

$代表了jQuery。



# jQuery选择器

所有的选择器都以美元符开头。

分为两种：

1、元素选择器。

2、`#id`选择器。

3、`.class`选择器。

元素选择器的。

```
$("p")
```

这个表示选取所有的`<p>`元素。

下面这段代码表示，点击按钮后，所有的`<p>`元素都被隐藏。

```
$(document).ready(function(){
  $("button).click(function() {
    $("p").hide();
  });
});
```

`#id`选择器的。

```
$("#test")
```

`.class`选择器。

```
$(".test")
```



# jQuery事件

jQuery的设计主要就是为了做事件处理的。

什么叫事件？

页面对不同访问者的响应就叫事件。

例如：

在元素上移动鼠标。

选取单选按钮。

点击元素。

常见的事件有：

1、鼠标事件。

```
click
dblclick
mouseenter
mouseleave
```

2、键盘事件。

```
keypress
keydown
keyup
```

3、表单事件。

```
submit
change
focus
blur 失去焦点的时候。
```

4、文档和窗口事件

```
load
resize
scroll
unload
```

## 常见的jQuery事件方法

1、`$(document).ready()`

这个是表示文档加载完成后执行的函数。

2、click。





# 参考资料

1、菜鸟教程

https://www.runoob.com/jquery/jquery-selectors.html

2、jQuery UI。

http://www.runoob.com/jqueryui/api-easings.html