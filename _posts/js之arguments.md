---
title: js之arguments
date: 2018-12-22 14:20:17
tags:
	- js
---



arguments是对象，不能显式创建，只有在函数里才能用。

函数的arguments对象并不是一个数组。但是使用起来很像数组。

类似Array，但是除了length方法之外，其他的Array的方法都没有。

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



js是不会对函数传参个数进行语法检查的。



什么是callee？是arguments对象的一个属性。

arguments对象的数据结构是这样的：

```
interface IArguments {
    [index: number]: any;
    length: number;
    callee: Function;
}
```

测试：

```
function func() {
    console.log(arguments.callee);
}

func();
```

结果：

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ node app.js  
[Function: func]
```

返回的就是函数本身。

我们可以用它来验证形参个数跟实际传递的参数个数是否相等。

```
function func(p1, p2) {
    if(arguments.length === arguments.callee.length) {
        console.log("param number is right");
    } else {
        console.log("param number is not right");
    }
}

func();
```



参考资料

1、javascript arguments(callee、caller) 详解

https://juejin.im/entry/58184ccda22b9d00679976c0