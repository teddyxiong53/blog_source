---
title: css学习
date: 2018-01-17 18:08:02
tags:
	- css

---



css这一块一直没怎么了解，现在系统快速过一遍。

# 为什么需要css

之前web上是没有css的，只有html标签。但是以前的页面也基本上没有太多的色彩、漂亮的排版这些东西。但是随着互联网的普及，普通用户对于网页内容是有审美述求的，这个时候，w3c组织就为了满足这种需求，提供了一些用来装饰html的标记，例如strong、font等等。

这个时候，程序员就麻烦来了。

1、为了装饰一个text，得写很多的标签。麻烦。

2、多个地方写一样的东西，不能重用。

3、这些标签在传输的时候，也是要占用带宽的，一个html文件里，大部分反而是格式性的东西。真正的内容不到十分之一。

w3c为了解决上面这3个问题，就提出了css这个东西。分别是如何解决的呢？

1、多个标签的问题。

css采用一条条规则来装饰各个html元素。如下：

```
<style type="text/css">
	p {
		font-size:20px;
		color:red;
	}
</style>
```

这样把内容和样式就分离开了。

2、重用问题。这个很明显。样式都提取到单独文件了，重用就很容易了。

3、也是一起解决了。

# css语法规则

我们还是以这个为例。

```
p 
{
		font-size:20px;
		color:red;
}
```

css规则就是两个部分。

p叫做选择器。

大括号里的每一条叫做声明。

css里的注释是`/**/`。

css可以写在单独的文件里，也可以在html文件里写。



id选择器和class选择器

如果你要给html元素使用css，就需要指定id和class这2个属性。

id是每个元素唯一，class则是可以多个一样，是为一组。

id用井号，class用的是点号。



如何插入css呢？

有三种方式：

1、内联。

2、内部。

3、外部。

优先级1高于2高于3 。



# css技巧

less和scss这样的预处理器在工作的时候，需要绕的路比较长。

直接使用css速度会更快。

需要一些css技巧来减少重复规则。

在布局中标准化样式流程。

不仅可以帮助你高效地创建自己的框架，而且可以解决许多常见的问题。



## 使用css重置

css重置库，例如normalize.css。已经被使用了很多年了。

它们可以为你的网站提供一个比较清晰的标准。

来确保跨浏览器的一致性。

大多数项目不需要这些库的所有规则，可以通过一条简单的规则来应用于所有的元素。

删除所有margin、padding来改变浏览器默认的盒模型。

```css
* {
	box-sizing: border-box;
	margin: 0;
	padding: 0
}
```

## 继承盒模型

让盒模型从html继承

```css
html {
	box-sizing: border-box;
}
*,*:before, *:after {
    box-sizing: inherit;
}
```

## body加入line-height样式

不断的重复声明，会导致效率的降低。

最好是嘴一下项目规划和组合规划。

这样会让css更加流畅。

要实现这个目标，就需要理解级联（cascade）。

要让在通用选择器写的规则，可以被其他地方继承。

行间距line-height 可以作为整个项目的一个属性。

不仅可以减小代码量，而且可以给你的网站的样式一个标准的外观。

```
body {
	line-height: 1.5;
}
```

注意，上面没有指定单位，它的作用是：

行间距为字体大小的1.5倍。

## 垂直居中任何元素

```
html, body {
	height: 100%;
	margin: 0;
}
body {
	align-items: center;
	display: flex;
}
```

## 使用svg图标

svg适用于所有分辨率。

所有浏览器都支持。

所以可以丢弃png、jpg等。

# css属性分类

## 文本、字体、颜色

字体

```
font-family
	需要考虑客户机器上是否安装了字体文件。
	可以排列多个字体，用逗号隔开。字体名字有空格的话，用引号括起来。
	最后一个是兜底的，建议放一个通用的名字。
	这个通用版名字，只有这么几个可以选择：
		serif 
		sans-serif
		monospace
font-size
	字体大小。
	有绝对大小，相对大小，长度，百分比。
	建议采用相对大小。使用em。
	
font-style
	有正常、斜体、倾斜体。
font-weight	
	粗体。
font	
	是把上面的都综合起来，一次性设置。
	font-family是必须的，而且必须在最后。
	font-size，如果有，必须是倒数第二个。
	其余的顺序随意。
	
line-height
	一个数字，一般是1.2 
```

文本

```
word-break	
	取值：normal、break-all、keep-all、break-word。
	normal：英文在空格处换行，中文任意地方都可以换行。
vertical-align
	上下对齐方式。
	取值：baseline（默认）、super（上标）、sub（下标）、top、bottom、middle、
text-align
	左右对齐方式。
	取值：left、right、center、justify（两侧对齐）。
	
text-transform
	大小写转换。
	取值：uppercase、lowercase、none、capitalize
text-shadow
	阴影设置。
text-decoration
	有几个：color、line、style。
text-indent
	缩进。段落的第一行。
text-justify
	这是之当text-align设置为两侧对齐的时候，是在单词（英文）前面加空格，还是字母前面加空格。
text-overflow
	文本溢出的截断。
```

颜色

```
background
	下面有
	-color
	-image
	-size
	-position
	-repeat
	-attachment
	-color必须是最后一个。
	
```

鼠标的样式

```
cursor:help 鼠标显示问号。
pointer 显示小手
progress  请等待
wait  系统繁忙。
move 拖拽
not-allowed 不能执行
```



## 大小、布局

大小

```
width/height
max-width
min-width
```

盒模型

```
border
outline
margin
padding

```

布局

```
float
clear
position
top/left/bottom/right
visibility
overflow
clip
transform
z-index
```

flex布局

```
display:flex
flex-direction
flex-wrap
flex-flow
align-items
justify-content
align-content
```

网格布局

表格布局



## 列表、表格

## 动画

# 参考资料

1、

http://www.runoob.com/css/css-intro.html

2、如何提升你的CSS技能，掌握这20个css技巧即可[完整版]

https://www.imooc.com/article/283531

3、

https://www.cnblogs.com/xuanku/p/css_attr.html