---
title: chrome之插件编写入门
date: 2018-08-31 20:42:56
tags:
	- chrome
typora-root-url:..\
---



要写chrome插件，需要js知识和最简单的html和css知识。

chrome还可以配合C++写的dll库来实现更加强大的功能，例如全屏幕截图。



chrome插件没有严格的项目结构要求，最低要求是有一个manifest.json文件。

通过chrome://extensions/ 这个地址进入到管理界面。勾选“开发者模式”。这样就可以用文件夹的方式来加载插件。

在开发中，代码有任何改动，都必须重新加载插件，只需要在插件管理页面按下ctrl+r来加载就好了。

#最简单的版本

我们在hbuilder里新建一个web项目。

先看manifest.json文件的写法。

一个最小的manifest.json文件就这么多，就这么点，就可以在chrome里正常加载了。

```
{
	"manifest_version": 2,
	"name": "demo",
	"version":"1.0.0",
	"description": "xhl chrome plugin demo",
	"icons": {
		"16":"img/icon.png",
		"48":"img/icon.png",
		"128":"img/icon.png"
	}
}
```

![](/images/chrome插件（1）-最小配置效果.png)

选择加载已解压的扩展程序，选择对应的文件夹就可以了。

如果有改动，点击右下角的刷新图标就可以。

当前的目录结构是这样：

```
λ ls
img/  manifest.json
```

img目录下就放了一张icon.png。

#加入popup

现在可以加入一个popup.html文件，这个就是你单机右上角图标弹出的一个小窗口的内容。

先写一个简单的。

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>popup页面</title>
		<meta http-equiv="content-type" content="text/html"/>
		<style>
			body {
				font-family: "微软雅黑";
				width:500px;
				min-height: 100px;
			}
			a {
				margin-right: 10px;
			}
		</style>
	</head>
	<body>
		<h1>这是一个popup页面</h1>
	</body>
</html>
```

然后在manifest.json里加上配置。

```
"browser_action": {
		"default_icon": "img/icon.png",
		"default_title": "这是一个chrome插件demo",
		"default_popup": "popup.html"
	}
```

刷新一下，现在就可以看到单击图标的效果了。

接下来做什么呢？

加入background.html

# background.html

新建一个background.html文件。

内容如下：

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>background页面</title>
		<meta http-equiv="content-type" content="text/html"/>
		<style>
			html,body {
				height: 100%;
				font-size: 16px;
			}
			body {
				font-family: "微软雅黑";
				margin: 0;
				padding: 0;
			}
			.container {
				width: 1024px;
				margin: 0 auto;
			}
		</style>
	</head>
	<body>
		<h1>这是一个背景页</h1>
		<div>
			<a href="#" id="test_cors">跨域演示</a>
			<a href="#" id="get_popup_title">获取popup页标题</a>
		</div>
		<script type="application/javascript" src="js/jquery-1.8.3.js"></script>
		<script type="application/javascript" src="js/background.js"></script>
	</body>
</html>
```

这里引入了2个js文件。jquery的我们直接放进来。

background.js，我们自己写。





# 参考资料

1、Chrome扩展demo

https://github.com/sxei/chrome-plugin-demo

2、chrome插件开发之调试

https://blog.csdn.net/qustdong/article/details/46046553