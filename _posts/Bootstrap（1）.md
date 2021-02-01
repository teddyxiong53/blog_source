---
title: Bootstrap学习
date: 2018-01-17 18:00:32
tags:
	- Bootstrap

---



# Bootstrap介绍

1、Bootstrap是一个用于快速开发web应用程序和网站的前端框架。

2、基于的技术是html、css和JavaScript。

3、2011年在github上开源。

# Bootstrap优势

1、移动设备优先。

2、主流浏览器都支持。

3、上手很容易。

4、可以自适应访问平台的特定。

# Bootstrap包的内容

1、基本结构。提供了一个带有网格系统、链接样式、背景的基本结构。

2、css。全局的css设置等等。

3、组件。包括了十几种可重用的组件。

4、js插件。

5、定制。

# 在线所见即所得编辑器

https://www.runoob.com/bootstrap/bootstrap-ui-editor.html

https://www.runoob.com/try/bootstrap/layoutit/

就用layoutit。菜鸟教程里集成了这个。

首先需要放一个row进去，然后才能放东西。



# tab切换页面

https://www.cnblogs.com/fqh123/p/11736421.html

```html
<li class="active">
    <a href="#get_mac" data-toggle="tab">获取MAC地址</a>
</li>
<li>
    <a href="#settings" data-toggle="tab">设置</a>
</li>
```

关键是href和data-toggle。

# bootstrap插件

bs自带了12中jquery的插件。

使用bs的data-* api来写，只要添加属性就可以使用这些插件。

大部分插件可以在不编写任何代码的情况下起作用。

只需要引入bootstrap.min.js就可以使用这些插件了。

data-* api是bootstrap里的一等api。

是你应该首选的方式。

如果你希望关闭这些data-* api，那么加上这样的代码：

```
$(document).off('.data-api')
```

如果只是关闭其中一类api，这样

```
$(document).off('.alert.data-api')
```

当然你可以用js原生的方式来写。

```
$('.btn.danger').button('toggle').addClass('fat')
```



有时候bootstrap会跟其他的ui框架一起使用。

在这样的情况下，可能产生命名空间冲突。



bootstrap为大多数插件的独特行为提供了自定义事件。

一般来说，这些事件有两种形式。

动词不定式

```
这个在事件开始的时候触发。
例如：show
这种事件提供了preventDefault的功能。

$('#myModal').on('show.bs.modal', function(e) {
	if(!data) {
		return e.preventDefault
	}
})
```



过去分词形式

这种是在动作执行完之后被触发。例如shown。



# css编码规范

https://www.runoob.com/bootstrap/bootstrap-css-codeguide-html.html

声明顺序

```
位置
盒模型
字体
颜色
其他
```

举例：

```
.xx {
	//位置
	position: absolute;
	top: 0;
	z-index: 100;
	//盒模型
	display:block;
	float: right;
	width: 100px;
	//字体
	font: sans-serif;
	line-height: 1.5;
	color: #333;
	text-align: center;
	//颜色
	background-color: #555;
	border: 1px;
	//其他
	opacity: 1;
}
```

其实，也是有一个从总体到细节的内在逻辑的。



# 代码实例

## tab

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="./css/bootstrap.min.css">
    <script src="js/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
</head>
<body>
    <ul class="nav nav-tabs" id="mytab">
        <li class="active"><a href="#aaa" data-toggle="tab">aaa</a></li>
        <li ><a href="#bbb" data-toggle="tab">bbb</a></li>
        <li class="dropdown">
            <a class="dropdown-toggle" href="#" id="mytabDrop1" data-toggle="dropdown">ccc<b class="caret"></b></a>
            <ul class="dropdown-menu" role="menu" aria-labelledby="mytabDrop1">
                <li><a href="#ddd" tabindex="-1" data-toggle="tab">ddd</a></li>
                <li><a href="#eee" tabindex="-1" data-toggle="tab">eee</a></li>
            </ul>
        </li>
    </ul>
    <div id="mytabContent" class="tab-content">
        <div id="aaa" class="tab-pane fade active">
            111
        </div>
        <div id="bbb" class="tab-pane fade">
            222
        </div>
        <div id="ddd" class="tab-pane fade">
            444
        </div>
        <div id="eee" class="tab-pane fade">
            555
        </div>
    </div>
</body>
</html>
```

## tooltip

提示工具（Tooltip）插件不像之前所讨论的下拉菜单及其他插件那样，它不是纯 CSS 插件。如需使用该插件，您必须使用 jquery 激活它（读取 javascript）。使用下面的脚本来启用页面中的所有的提示工具（tooltip）：

```

$(function () { $("[data-toggle='tooltip']").tooltip(); });
```





参考资料

1、

https://www.cnblogs.com/wulinzi/p/8303168.html

2、Bootstrap

https://zh.wikipedia.org/wiki/Bootstrap

3、

https://v3.bootcss.com/css/

4、Bootstrap 流式栅格系统

https://blog.csdn.net/ixygj197875/article/details/79439970

5、bootstrap实现分页（实例）

https://blog.csdn.net/qq_41485414/article/details/79622931

6、实现 Bootstrap 基本布局

https://www.cnblogs.com/haogj/p/4980353.html

7、中文文档

https://v3.bootcss.com/getting-started/

8、bootstrap组件之navbar

https://www.cnblogs.com/zhangbao/p/6593121.html