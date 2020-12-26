---
title: js之this
date: 2018-12-22 10:30:17
tags:
	- js
---





this是函数内部的一个特殊对象。它表示的是函数执行的上下文环境。

跟java这些语言里的this不太相同。

在js里，this不是固定不变的 。而是随着执行环境的改变而改变的。

**js里的this总是指向调用它所在方法的对象。**

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



# this instanceof 

通过`this instanceof Vue`来判断有没有new这个关键字的使用。

为什么可以这么做呢？

在js里，this是动态绑定的，也叫运行时绑定。

this可以是全局对象，当前对象或者任意对象。

这取决于函数的调用方式。

函数的调用方式有：

1、作为对象方法调用。

2、作为函数调用。

3、作为构造函数调用。

4、使用apply和call调用。

作为对象方法调用是这样

```
var point = {
    x:0,
    y:0,
    moveTo:function(x, y) {
        this.x = x
        this.y = y
    }
}
```

这里的this，就是当前对象，也就是point对象。

作为函数调用

```
function test(y) {
    this.x = y
}
log(x)//这个就是全局对象window.x
```

我们看另外一种情况

```
var point = {
    x:0,
    y:0,
    moveTo: function(x,y) {
        //内部函数
        var moveX = function(x) {
            this.x = x
        }
        var moveY  = function(y) {
            this.y = y
        }
        moveX(x)
        moveY(y)
    }
}
point.moveTo(1,1)
console.log("point.x:"+point.x)
console.log("point.y:"+point.y)
console.log("x:"+x)
console.log("y:"+y)
```

得到的结果是：

```
point.x:0
point.y:0
x:1
y:1
```

这内部函数的this，就是全局对象了。

这是因为没有明确的调用对象。js就绑定到默认的全局对象了。

为了解决这种问题，我们可以使用箭头函数。

```
//内部函数
        var moveX = (x) =>{
            this.x = x
        }
        var moveY  = (y)=> {
            this.y = y
        }
```

箭头函数是默认绑定外层的this的。

也可以用apply。但是箭头函数更好。



下面看看构造函数调用。

new是运算符，它做了这些事情

1、创建一个空的对象{}

2、设置该对象的构造函数为另外一个对象，`o.__proto__=Point.prototype`

3、将第一步的对象作为this的上下文。

4、如果该对象没有返回对象，则返回this。



apply和call，就是用来切换函数执行的上下文的。



`this instanceof Vue`

这句代码，我们可以这样分解

`this.__proto__`和`Vue.prototype`。

如果没有使用new，那么this指向全局对象。

全局对象肯定不是Vue的实例。这个判断返回false。

如果使用了new，我们应用上面new运算符的4个步骤。

```
o.__proto__ == this.__proto__  == Vue.prototype
```









参考资料

1、JavaScript 的 this 原理

http://www.ruanyifeng.com/blog/2018/06/javascript-this.html

2、详解 JavaScript的 call() 和 apply()

https://www.cnblogs.com/qiaojie/p/5746688.html

3、JavaScript的回调函数内部this的指向问题以及四种绑定this指向的方法

https://blog.csdn.net/Mr_28/article/details/78344321

4、从Vue源码学习JavaScript之this instanceof Vue

https://segmentfault.com/a/1190000019017266