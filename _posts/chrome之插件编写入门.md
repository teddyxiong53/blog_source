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





# 参考资料

1、Chrome扩展demo

https://github.com/sxei/chrome-plugin-demo