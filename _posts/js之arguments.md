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



再看例子。

```
class MyClass {
    constructor() {
        console.log(arguments);
    }
}

var c1 = new MyClass();
var c2 = new MyClass("c2");
var c3 = new MyClass(1,2);
```

运行：

```
[Arguments] {}
[Arguments] { '0': 'c2' }
[Arguments] { '0': 1, '1': 2 }
```

