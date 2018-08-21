---
title: html之全局属性
date: 2018-08-21 22:41:27
tags:
	- html

---



在html里，属性可以表达相当丰富的语义。属性也可以额外提供很多实用的功能。

全局属性一共16个。



#accesskey

相当于定义快捷键。

```
<div>
	<a href="http://www.baidu.com" accesskey="b">百度</a>
</div>
```

你按alt+b，就可以调整到百度。

# class

规定元素的一个或者多个类名。

多个类名之间用空格分开。



# dir



# id

如果一个文件里出现元素的id相同时，css是对所有的id都生效。而js代码则是对第一个生效。

```
<!DOCTYPE html>
<head>
	<meta charset="UTF-8">
	<title>document</title>
	<style>
		#test {
			color : red;
		}
	</style>
</head>

<body>
	<div id="test">aaaaaaaaaaa</div>
	<div id="test">bbbbbbbbbbb</div>
	<script>
		var oDiv = document.getElementById("test");
		oDiv.style.color = "green";
	</script>
</body>
```



# lang

规定元素内容的语言。

en或者zn



# 参考资料

1、HTML的16个全局属性

https://blog.csdn.net/long_ge_cool/article/details/50251215