---
title: Bootstrap学习
date: 2018-01-17 18:00:32
tags:
	- Bootstrap

---



# 1. Bootstrap介绍

1、Bootstrap是一个用于快速开发web应用程序和网站的前端框架。

2、基于的技术是html、css和JavaScript。

3、2011年在github上开源。

# 2. Bootstrap优势

1、移动设备优先。

2、主流浏览器都支持。

3、上手很容易。

4、可以自适应访问平台的特定。

# 3、Bootstrap包的内容

1、基本结构。提供了一个带有网格系统、链接样式、背景的基本结构。

2、css。全局的css设置等等。

3、组件。包括了十几种可重用的组件。

4、js插件。

5、定制。

#4、HelloWorld

参考我自己的《Python之Django学习（六）开发一个BVDN网站》文章里描述的内容，在树莓派上搭建好Bootstrap的环境。

目录结构是这样的：

```
pi@raspberrypi:~/udisk/work/bvdn$ tree -L 2
.
├── base.html
└── static
    ├── css
    ├── fonts
    └── js

```



写base.html内容。

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>bootstrap helloworld</title>
		<link rel="stylesheet" href="/static/css/bootstrap.css">
		<script type="text/javascript" src="/static/js/jquery.js"></script>
		<script type="text/javascript" src="/static/js/bootstrap.js"></script>
	</head>
	<body>
		<h1>hello bootstrap</h1>
	</body>
</html>
```

不过在实际的使用中，我们一般是用其他的cdn提供的Bootstrap资源。这样更快。

