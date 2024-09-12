---
title: css之scss
date: 2021-01-06 11:34:11
tags:
	- css

---

--

# 在线练习

https://jsfiddle.net/boilerplate/scss

# **Scss 与 Sass的区别**

Sass 和 Scss 其实就是同一种东西，我们平时都称之为 Sass，两者之间不同之处主要有以下两点：

1、文件扩展名不同，Sass 是以“.sass”后缀为扩展名，而 Scss 是以“.scss”后缀为扩展名。

2、语法书写方式不同，Sass 是以严格的缩进式语法规则来书写，不带大括号({})和分号(;)，而 Scss 的语法书写和我们的CSS 语法书写方式非常类似。

声明变量

```
$width: 50px;
```

插值，用`#{}`

```
$name: foo;
p.#{$name} === p.foo
```

继承extend

extend只能继承选择器。

```
.error {
	backgroud-color: red;
}
.seriousError {
	@extend .error;
	border-width: 3px;
}
```



# 基本语法

## 变量

```
//数据类型
$w: 100px;               //数值类型，带单位
$img-path: './src/images';  //字符串
$bgc: #ffaa;              //颜色
$is-light: true;            //bool类型
$var:null;                  //null
$size-list: xs, sm,md, lg, xl;  //list类型
$map: (key1:value1, key2: value2)  //map类型

$var1: var; // 一个变量的值可以是另外一个变量
```

## 条件判断

```
$dark-theme: true
@if $dark-theme {
	//...
}
```



https://juejin.cn/post/7242258285159186488

# 参考资料

1、SCSS语法

https://www.jianshu.com/p/3259976b414b

2、SASS用法指南

https://www.ruanyifeng.com/blog/2012/06/sass.html