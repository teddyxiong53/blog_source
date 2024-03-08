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



Bootstrap是一个开源的前端框架，最初由Twitter团队开发并维护。它提供了一组用于快速、简化Web开发的HTML、CSS和JavaScript工具。Bootstrap的目标是使网站和Web应用程序的开发变得更加简单、快捷，并确保它们在不同设备和屏幕大小上都能够良好地工作。

以下是Bootstrap的一些主要特点和组成部分：

1. **响应式设计：** Bootstrap的设计是响应式的，能够适应不同屏幕大小和设备类型，包括桌面、平板和移动设备。

2. **组件库：** Bootstrap提供了丰富的UI组件，如导航栏、按钮、表格、表单、模态框等，这些组件都经过样式化和预定义，可以轻松地集成到项目中。

3. **网格系统：** Bootstrap引入了一个强大的网格系统，用于实现页面布局。这使得开发人员能够轻松地创建灵活的、栅格化的页面布局，适应不同的屏幕尺寸。

4. **基于Sass：** Bootstrap的CSS样式是基于Sass（Syntactically Awesome Stylesheets）预处理器构建的，这使得定制和扩展样式变得更加灵活和方便。

5. **插件和扩展：** Bootstrap支持各种插件和扩展，如日期选择器、图表库等，这些可以增强应用程序的功能。

6. **社区支持：** 由于Bootstrap是开源的，拥有庞大的社区支持。这意味着您可以在社区中找到大量的文档、教程和第三方资源，帮助您更好地使用和理解Bootstrap。

7. **跨浏览器兼容性：** Bootstrap经过广泛测试，确保在主流的现代Web浏览器中表现良好。

使用Bootstrap，开发人员可以更快速地构建具有现代外观和响应式设计的网站和应用程序，同时减少了对于自定义CSS和JavaScript的需求。通过利用Bootstrap的模块化和可定制的特性，您可以根据项目的需要灵活地使用框架的不同部分。



# Bootstrap优势

1、移动设备优先。

2、主流浏览器都支持。

3、上手很容易。

4、可以自适应访问平台的特定。

# bootstrap的原理

Bootstrap的原理涉及到它是如何通过HTML、CSS和JavaScript组合在一起，以及如何利用其网格系统、样式和组件库来简化和加速前端开发。以下是Bootstrap的一些基本原理：

1. **HTML结构：** Bootstrap的基本结构是建立在HTML之上的。您使用标准的HTML标记，但可以通过引入Bootstrap提供的类和元素来快速实现特定样式和功能。

2. **CSS样式：** Bootstrap的样式是通过CSS实现的，这些样式定义了页面的外观和排版。框架使用Sass进行样式预处理，使得样式表具有可维护性和可扩展性。您可以通过引入Bootstrap的CSS文件或仅引入所需的样式来使用其样式。

3. **JavaScript插件：** Bootstrap包含一些可选的JavaScript插件，用于实现交互式和动态的功能。这些插件通常基于jQuery，并用于处理例如模态框、轮播、下拉菜单等组件的行为。您可以选择根据需要引入这些插件，也可以根据项目的需求自定义它们。

4. **网格系统：** Bootstrap的网格系统是其布局的基础。通过使用容器、行和列的组合，开发人员可以轻松地实现响应式设计。网格系统允许您定义不同屏幕尺寸下的布局，确保您的应用程序在各种设备上都能够良好地显示。

5. **响应式设计：** Bootstrap的响应式设计是通过媒体查询和弹性布局来实现的。这使得页面能够适应不同的屏幕尺寸，并根据设备特性进行调整。

6. **定制和主题：** Bootstrap允许您通过修改Sass变量或使用定制的构建工具来创建自定义主题。这使得您可以根据项目需求调整颜色、字体、边框等样式。

总体而言，Bootstrap的原理在于提供一种结构化和标准化的方法，使开发人员能够快速构建现代、响应式的Web应用程序，而无需从头开始编写所有的HTML、CSS和JavaScript代码。通过使用预定义的类、组件和样式，Bootstrap简化了前端开发的复杂性，同时提供了足够的灵活性，以满足各种项目需求。

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



# 为什么使用很多的div

使用很多的 `<div>` 元素在前端开发中有几个主要原因：

1. **结构和布局：** `<div>` 元素是HTML中的块级元素，常用于创建页面的结构和布局。通过嵌套和组合 `<div>` 元素，开发人员可以实现复杂的页面结构，将页面划分为不同的区块，从而更容易管理和维护代码。

2. **样式和布局调整：** `<div>` 元素可以用于应用样式和调整布局。开发人员可以通过为 `<div>` 添加类来应用预定义的样式，或者通过内联样式直接在元素上指定样式属性。这种方式使得页面样式更加灵活，易于调整和定制。

3. **响应式设计：** 使用 `<div>` 元素配合Bootstrap等前端框架的网格系统，可以实现响应式设计。响应式设计确保页面能够适应不同的屏幕尺寸和设备类型，提供更好的用户体验。网格系统通常要求使用 `<div>` 元素来创建行和列，以便定义页面的布局。

4. **JavaScript交互：** 在前端开发中， `<div>` 元素通常用于容纳JavaScript交互所需的内容。例如，一个模态框通常会被包装在一个 `<div>` 中，以便通过JavaScript来控制显示和隐藏。

5. **组件化开发：** 使用 `<div>` 元素有助于实现组件化开发的思想。通过将不同的功能单元封装在 `<div>` 中，可以更轻松地复用和维护代码。这有助于提高代码的可维护性和可读性。

尽管 `<div>` 元素在前端开发中是一种非常灵活和强大的工具，但过度使用也可能导致 HTML 结构复杂，增加代码的阅读难度。因此，在实际开发中，开发人员通常会努力保持代码的简洁性和可读性，避免不必要的嵌套和过多的 `<div>` 元素。

# 参考资料

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