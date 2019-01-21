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



jQuery的意义是什么？为什么需要jQuery？

现在又为什么不再需要了？



jQuery的设计宗旨是：用更少的代码做更多的事情。

jQuery封装了常用的功能代码，优化了html文档参照，事件处理，动画设计和ajax交互。



jQuery的核心特性可以总结为：

1、具有独特的链式语法。

2、短小清晰的多功能接口。

3、具有高效的css选择器。

4、拥有便捷的插件机制和丰富的插件。

5、兼容主流浏览器。



jQuery的具体作用：

1、取得页面里的元素。不用js库，自己写代码遍历dom，需要写很多行的代码。

2、修改界面的外观。浏览器支持的css标准不同的时候，写css代码就很烦人。jQuery帮我们解决了这种问题。

3、改变页面的内容。

4、响应用户的界面操作。

5、为页面添加动态效果。

6、ajax。



jQuery的发展历史：

1、2005年8月，John Resig提议改进Prototype里的Behavior库。于是他在博客上发表了自己的想法，并用3个简单的例子做了流程说明。

（Prototype这个库，已经退出历史舞台了。被jQuery完全取代了。）

这篇博客在业内引起了广泛关注。

2、2006年1月14日，John以jQuery发布了自己的程序库。

3、8月份，jQuery有了第一个稳定版本。已经开始支持css选择符、事件处理和ajax提交。

4、微软、诺基亚等大公司也参与了进来。



工作原理

jQuery的模块分为3部分：

1、入口模块。

2、底层支持模块。

3、功能模块。



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



# 和普通js代码对比

jQuery能做的。普通js代码也可以做到。只是麻烦一点。

怎么个麻烦法呢？

我们看看对比。

加载dom

```
//普通js
function my_onload() {
	console.log("xx");
}
window.onload = my_onload;
```

```
//jquery
$(document).ready() {
    
}
```

获取id

```
//普通js
document.getElementByID("xx");
```

```
//jquery
$("#xx")
```

获取class

```
//普通js
无法获取
```

```
//jQuery
$(".xx")
```

后去tagName

```
//普通js
document.getElementByTagName("xx");
//jquery
$("xx")
```

创建对象并加入到文档里。

```
//普通js
var para = document.createElement("p");
document.body.appendElement(para);
```

```
//jquery
$("p").append('<p>xxx</>');
```







# 参考资料

1、菜鸟教程

https://www.runoob.com/jquery/jquery-selectors.html

2、jQuery UI。

http://www.runoob.com/jqueryui/api-easings.html

3、jQuery的具体作用

https://blog.csdn.net/qq_15016387/article/details/82378054

4、Prototype这个JS库的现状如何？

https://www.zhihu.com/question/21165560

5、jquery和javascript的区别(常用方法比较)

https://blog.csdn.net/yyy183833/article/details/52413357