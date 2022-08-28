---
title: layui（1）
date: 2020-08-27 08:36:08
tags:
	- 网页

---

--

因为layoutit布局得到的文件，在bootstrap3就不能正常使用了。

在寻找解决方法的时候，找到这个layui。B站上也找到不错的教程视频。

所以学习一下这个的使用。

自己用来写一个博客系统。

官网文档在这里：

https://layuion.com/docs/

Layui 区别于一众主流的前端框架，却并非逆道而行，而是信奉返璞归真之道。确切地说，它更多是面向于追求简单的务实主义者，他们无需涉足各类构建工具，只需面向浏览器本身，即可轻松掌握页面所需的元素与交互，进而信手拈来。

他们这个设计理念很符合我的需要。够用就好。

layui 兼容人类正在使用的全部浏览器（IE6/7 除外），可作为 Web 界面速成开发方案。

核心文件就2个

```
layui/
  ├─css
  │  └─layui.css   # 核心样式库
  └─layui.js       # 核心模块库
```

现在版本是2.7.6，直接官网下载即可。

先写一个HelloWorld。

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8" />
		<title>test-layui</title>
		<script src="./layui-v2.7.6/layui/layui.js" type="text/javascript"></script>
		<link rel="stylesheet" href="layui-v2.7.6/layui/css/layui.css">
	</head>
	<body>
		<script>
		layui.use(['layer', 'form'], function(){
		  var layer = layui.layer;
		  var form = layui.form;
		  
		  layer.msg('Hello World');
		});
		</script> 
	</body>
</html>
```



Layui 采用自身轻量级模块化规范，

并非是有意违背 CommonJS 和 ES Module ，

而是试图以更简单的方式去诠释高效，

这种对返璞归真的执念源于在主流标准尚未完全普及的前 ES5 时代，

后来也成为 Layui 独特的表达方式，而沿用至今。

```
// 定义模块（通常单独作为一个 JS 文件）
layui.define([modules], function(exports){
  //…
  
  exports('mod1', api);
});  
 
// 使用模块
layui.use(['mod1'], function(args){
  var mod1 = layui.mod1;
  
  //…
});
```

作者讲layui为什么下线。

https://www.zhihu.com/question/488668647/answer/2159962082



layui 是 es3/es5 时代 AMD+jQuery 的产物，所以它无论是在管理模块还是视图渲染上，都是在向原生妥协，一个组件从 DOM 查询到数据的动态变更，效率已不合时宜。



参考资料

1、

