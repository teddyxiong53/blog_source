---
title: css之less
date: 2020-12-31 09:21:11
tags:
	- css

---

1

less是一种预处理语言，用来生成css文件的。

为什么不直接用css语言？

因为灵活性不足。比较繁琐。而且对变化应对比较差。

less通过js脚本转成css文件。

less本身像一门编程语言，可以进行更灵活的编程。

css预处理语言，主要有三种：saas、less、stylus。

saas诞生最早。

less受saas影响。

less功能相对少一些。诞生学习成本低一些。

我现在看less，是因为看到cnode里用到了这种。

不然把这个作为学习css预处理语言的切入点。



引入less

有两种方方法：

1、在页面里引入less.js文件。`<script src="//cdnjs.cloudflare.com/ajax/libs/less.js/2.7.2/less.min.js"></script>`

2、安装命令行工具，npm i -g less

转换命令：`lessc 1.less > 1.css`



LESS是一个CSS预处理器，可以为网站启用可自定义，可管理和可重用的样式表。

CSS预处理器是一种脚本语言，可扩展CSS并将其编译为常规CSS语法，以便可以通过Web浏览器读取。 它提供诸如变量，函数， mixins 和操作等功能，可以构建动态CSS。

安装less：

```
npm i -g less less-cli
```

# HelloWorld

当前目录新建一个index.html文件。

```
<!doctype html>
<head>
	<link rel="stylesheet" href="style.css" type="text/css" />
</head>
<body>
	<h1>Welcome to W3Cschool</h1>
	<h3>Hello!!!!!</h3>
</body>
</html>
```

style.less内容

```
@primarycolor: #FF7F50;
@color:#800080;
h1{
color: @primarycolor;
}
h3{
color: @color;
}
```

编译less

```
lessc.cmd .\style.less .\style.css
```

得到的style.css文件内容

```
h1 {
  color: #FF7F50;
}
h3 {
  color: #800080;
}
```

# 规则嵌套

```
.container {
	h1 {
	
	}
	p {
	
	}
	.myclass {
		h1 {
		
		}
		p {
	
		}
	}
	
}
```

这样编译得到的

```
.container h1 {

}
.container p {

}
.container .myclass h1 {

}
.container .myclass p {

}
```

# 算术运算

就是可以进行加减乘除。

# 转义

跟在`~`后面的内容，就被转义。

```
p {
  color: ~"green";
}
```

等价于

```
p {
  color: green;
}
```

# 命名空间和访问器

style.less这样写：

```
.class1 {
    .class2 {
        .val(@param) {
            font-size: @param;
            color: green;
        }
    }
}
.myclass {
    .class1 > .class2 > .val(20px)
}
```

html里这样使用

```
<p class="myclass">xx</p>
```

编译得到的

```
.myclass {
  font-size: 20px;
  color: green;
}
```

# 变量范围

从本地作用域先搜索，找不到，再找父作用域。

```
@var: @a;
@a: 15px;

.myclass {
    font-size:@var;
    @a:20px;
    color: green;
}
```

这个最后得到的是20px，而不是15px。因为括号里找得到。

```
.myclass {
  font-size: 20px;
  color: green;
}
```

# 引入文件

@import

# 变量

@xxx :val 这样来定义变量。

选择器、url、import后面等都可以使用变量。

总体来说，类似于C语言的宏展开。

# 扩展

`:extend`是less的一个伪类。

用来扩展一个选择器。

```
h2 {
    &:extend(.style);
    font-style: italic;
}
.style {
    background: green;
}
```

效果是：

```
h2 {
  font-style: italic;
}
.style,
h2 {
  background: green;
}
```

# 混合mixin

mixin类似于其他语言里的函数。

```
.p1 {
    color: red;
}

.p2 {
    background: #64d9c0;
    .p1();
}
```

效果

```
.p1 {
  color: red;
}
.p2 {
  background: #64d9c0;
  color: red;
}
```

# 混合参数

```
.border(@width; @style; @color) {
    border: @width @style @color;
}

.myheader {
    .border(2px; dashed; green);
}
```

效果

```
.myheader {
  border: 2px dashed green;
}
```

# &详解

使用less我们就会经常用到&，它的用途有很多，今天写组件的时候遇到了几个问题所以整理一下

内层选择器前面的 & 符号就表示**对父选择器的引用**。

在一个内层选择器的前面，如果没有 & 符号，则它被解析为父选择器的后代；

如果有 & 符号，它就被解析为父元素自身或父元素的伪类。

同时用在选择器中的&还可以反转嵌套的顺序并且可以应用到多个类名上



&基本可以替换为父选择器。

````
.myclass {
	&:after {
		
	}
}
````

效果是

```
.myclass:after {

}
```



```
.demo {
	&-title {
		text-align: center;
	}
}
```

效果是

```
.demo-title {
	text-align: center;
}
```





参考资料

1、学习Less-看这篇就够了

https://juejin.cn/post/6844903520441729037

2、Less 教程

https://www.w3cschool.cn/less/

3、less 的 & 详解

https://www.jianshu.com/p/127b0974cfc3