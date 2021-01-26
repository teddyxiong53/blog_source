---
title: html之标签分类
date: 2021-01-22 11:10:11
tags:
	- html

---

--

# 标签分类

html标签可以分为这些类：

```
基础标签
	就9个。
	<!DOCTYPE>
	html
	title
	body
	h1/h6
	p
	br
	hr
	<!-- -->
格式标签
	就是加粗斜体这些，不少都废弃了。
	不重要，知道是什么意思就行了。一般不用。
	cite：引用。
	code
	del：删除线。
	em：强调。
	pre：这个是预格式。里面的空格会被保留。
	sub:下标。
	sup:上标。
	u：下划线。
	
表单标签
	form
	input
	textarea
	button
	select：下拉列表
	optgroup：下拉列表里的选项组。
	option；选项组里的选项。
	label：给input配套的。
	fieldset：把form里的元素圈起来的边框。
	legend：fieldset的标题。
	
框架标签
	iframe 目前就这一个了。其他的全部被废弃。
图像标签
	img
	canvas：通过脚本绘制区域。
	figure：对元素进行组合。
音视频标签
	audio
	video
	track ：字幕。
	
链接标签
	a
	link：资源文档。
	main：定义文档的主体部分。
	nav：定义导航链接。
	
列表标签
	ul
	ol
	li
	menu
表格
	table
	caption：表格标题。
	th
	tr
	td
	thead
	tbody
	tfoot
	col
样式及分块
	style
	div
	span
	header
	footer
	section
	article
	aside
	details
	dialog
	
元信息标签
	head
	meta
	base
程序
	script
	embed
```



# button和input button区别

<button> 标签定义的是一个按钮。

在 button 元素内部，可以放置文本或图像。这是<button>与使用 input 元素创建的按钮的不同之处。

无意中把<button>标签放到了<form>标签中，你会发现点击这个button变成了提交，相当于<input type="submit"/>

 请始终为按钮规定 type 属性。Internet Explorer 的默认类型是 "button"，而其他浏览器中（包括 W3C 规范）的默认值是 "submit"。

  这一点参见上面第二句标红的话就明白什么意思了。

  不要把<button>标签当成<form>中的input元素。

# 参考资料

1、

https://www.runoob.com/tags/ref-byfunc.html

2、

https://blog.csdn.net/qq_20662113/article/details/53010530