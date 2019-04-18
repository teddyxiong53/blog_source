---
title: js之this
date: 2018-12-22 10:30:17
tags:
	- js
---





this是函数内部的一个特殊对象。它表示的是函数执行的上下文环境。

跟java这些语言里的this不太相同。

在js里，this不是固定不变的 。而是随着执行环境的改变而改变的。

js里的this总是指向调用它所在方法的对象。

因为this是在函数运行时，自动生成的一个内部对象。只能在函数内部使用。



先看例子。

```
<html>
<head>
	<script>
        var obj = {
			foo: function() {
				console.log(this.bar);
			},
			bar: 1
		};
		var foo = obj.foo;
		var bar = 2;
		console.log("obj.foo");
		obj.foo();
		console.log("foo");
		foo();
	</script>
</head>

<body>
</body>
</html>
```

输出结果是1和2 。

关键就是里面的this关键字。

obj.foo()是在obj的范围内运行。而foo()是在全局环境里运行。



js里之所有有this，跟内存里的数据结构有关系。

```
var obj = {foo: 5};
```

对于这个代码， js引擎会先在内存里生成一个对象{foo:5}，然后把地址赋值给变量obj。

但是属性的值，可能是一个函数。这就让问题复杂化了。





1、在网页全局域里调用函数，this表示的是window。

```
<html>
<head>
	<script>
        var color = "red";
        function sayColor() {
            console.log(this.color);
        }
        sayColor();
	</script>
</head>

<body>
</body>
</html>
```



apply和call函数都为了改变函数内部的this指向。

ECMA规范为所有的函数都包含了这2个方法（不是通过继承而来）。

这2个函数都是在特定的作用域里调用函数，可以改变函数的作用域。

call和apply的区别：

call是不定长参数。apply参数是一个数组。



实际上是改变了函数内this的值。

```
<html>
<head>
	<script>
        function add(x, y) {
			return x+y;
		}
		function myAddCall(x, y) {
			return add.call(this, x, y);
		}
		function myAddApply(x, y) {
			return add.apply(this, [x,y]);
		}
		console.log(myAddCall(1,2));
		console.log(myAddApply(3,4));
	</script>
</head>

<body>
</body>
</html>
```

改变函数作用域。

```
<script>
        var name = "allen";
		var obj = {
			name: "bob"
		};
		function sayName() {
			return this.name;
		}
		console.log(sayName.call(this));
		console.log(sayName.call(obj));
	</script>
```



# 我的理解

我现在用jquery写一个投票网站。

关于this，就碰到了不少的问题。

我做实验，得到这些结论：

在浏览器里：

```
1、在script里，任何函数外面，this表示的是window。在普通函数里，也是window。
2、在$(document).ready(function() {里。是document。
3、在这里：$('input[type=radio]').each(function() {
        console.log(this)
        表示就是一个个的input。
```



在nodejs里。

```
this默认是global。

```





参考资料

1、JavaScript 的 this 原理

http://www.ruanyifeng.com/blog/2018/06/javascript-this.html

2、详解 JavaScript的 call() 和 apply()

https://www.cnblogs.com/qiaojie/p/5746688.html

3、JavaScript的回调函数内部this的指向问题以及四种绑定this指向的方法

https://blog.csdn.net/Mr_28/article/details/78344321

