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



css之所以一定要求分号做结尾。是因为css大部分情况下，是提高的压缩版本。如果没有分号，就乱了。



bootstrap的流式栅格系统



bootstrap由css和js构成。js需要依赖jquery。

模板文件。

```
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>Bootstrap 101 Template</title>

    <!-- Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 shim 和 Respond.js 是为了让 IE8 支持 HTML5 元素和媒体查询（media queries）功能 -->
    <!-- 警告：通过 file:// 协议（就是直接将 html 页面拖拽到浏览器中）访问页面时 Respond.js 不起作用 -->
    <!--[if lt IE 9]>
      <script src="https://cdn.jsdelivr.net/npm/html5shiv@3.7.3/dist/html5shiv.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/respond.js@1.4.2/dest/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <h1>你好，世界！</h1>

    <!-- jQuery (Bootstrap 的所有 JavaScript 插件都依赖 jQuery，所以必须放在前边) -->
    <script src="https://cdn.jsdelivr.net/npm/jquery@1.12.4/dist/jquery.min.js"></script>
    <!-- 加载 Bootstrap 的所有 JavaScript 插件。你也可以根据需要只加载单个插件。 -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js"></script>
  </body>
</html>
```



官方的例子在bootstrap源代码的docs/example目录下。



接下来还是参考菜鸟教程学一遍。





navbar

navbar是指导航条。

它在移动设备上显示为折叠字体，在宽屏幕上水平展开。



值得深入掌握的例子。

```
轮播。
	这个导航栏是static的。
dashboard。
	这个到导航栏是fix top的。
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