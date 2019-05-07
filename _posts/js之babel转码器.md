---
title: js之babel转码器
date: 2019-05-07 14:37:17
tags:
	- js
---

1

babel转码器就是用来把es6代码转成es5代码的工具。

这个意味着，你可以放心地用es6来写代码，不用关心兼容性的问题。

怎么使用babel呢？

你需要一个配置文件，.babelrc。放在项目的根目录。

这个文件的基本格式是：

```
{
  "presets": [],
  "plugins": []
}
```

presets用来设置转码规则，

例如，这样来安装es2015的转码规则

```
npm install --save-dev babel-preset-es2015
```

我们修改.babelrc文件。

```
{
  "presets": [
  	"es2015"
  ],
  "plugins": []
}
```

安装命令行工具

```
npm install --global babel-cli
```

我们写一个简单的箭头函数，这个是es6的语法，我们看看怎么给我们进行转码。

```
input.map(item=>item+1)
```

转码：

```
hlxiong@hlxiong-VirtualBox ~/work/test/babel $ babel ./app.js 
"use strict";

input.map(function (item) {
  return item + 1;
});

```



参考资料

1、Babel 入门教程

http://www.ruanyifeng.com/blog/2016/01/babel.html