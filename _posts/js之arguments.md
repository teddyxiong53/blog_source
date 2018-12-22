---
title: js之arguments
date: 2018-12-22 14:20:17
tags:
	- js
---



arguments是对象，不能显式创建，只有在函数里才能用。

函数的arguments对象并不是一个数组。

```
function add(a,b) {
	console.log(typeof arguments);
	for(var attr in arguments) {
		console.log(attr + ": " + arguments[attr]);
	}
}
add(10,20);
```

从输出可以看出arguments是一个对象，不是数组。

这个这个数组的属性名是自然数。

js不要求形参和实参个数一样。

```
function add(a,b) {
	if(arguments.length == arguments.callee.length) {
		return a+b;
	} else {
		return "arguments error";
	}
}
console.log(add(10));
```



