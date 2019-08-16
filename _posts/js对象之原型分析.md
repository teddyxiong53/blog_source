---
title: js之原型分析
date: 2019-04-19 22:14:25
tags:
	- js

---



![](../images/js原型层次.png)



原型链的终点是null。



跟大部分面向对象的语言不同，js里没有引入类的概念。

但是js里大量使用了对象。

为了保证对象之间的联系，js引入了原型和原型链的概念。

在java里，创建一个对象是这么写的：

```
Foo foo = new Foo();
```

为了让js看起来像java，js也引入了new操作符。

```
var foo = new Foo();
```



看一个实例。

```
function Dog(name, color) {
  this.name = name;
  this.color = color;
  this.bark = function() {
    console.log("wangwang~");
  }
}
var dog1 = new Dog("dog1", "black");
var dog2 = new Dog("dog2", "white");
```

我们上面定义2条狗，一个黑的，一个白的。

它的bark方法是一样的。

其实是可以抽取出来的。如果不抽取出来，这样对象就要多占用一部分内存。

```
2019年8月13日16:36:09
我最近学习了glib的GObject系统。
这里面的对象系统，Class和Instance是分开定义的。
Class就跟js里的原型是类似的，所有的Instance共用一个Class，这样就节省了空间了。
```



所以就引入了原型。

原型叫prototype。

```
对象.__proto__ === 类（函数）.prototype
```



我们提取Dog的原型。

```
function Dog(name, color) {
  this.name = name;
  this.color =color;
}
Dog.prototype.bark = function() {
  console.log("wangwang");
}
```

用原型链实现了继承关系。



js里的继承非常灵活，其中最常用的是组合继承。

```
function Dog(name, color) {
  this.name = name;
  this.color =color;
}
Dog.prototype.bark = function() {
  console.log("wangwang");
}
function Husky(name, color, weight) {
  Dog.call(this, name, color);
  this.weight = weight;
}
Husky.prototype = new Dog();
```



不同于java，JavaScript采用了基于原型的继承方式。

为什么要这么做？



js是一种多样化的编程语言。

它拥有面向对象和函数式这两种编程风格。

你可以使用任意一种风格来编程。

但是这两种风格不能很好地融合。

例如，你不能同时使用new（面向对象风格）和apply（函数式风格）。

原型继承是作为连接这两种风格的桥梁。



基于类的继承的问题

js里，每个函数都可以被当成构造函数来使用。

所以，我们需要区分普通函数调用和构造函数调用。

这边一般是用new关键字来进行区分。

但是，这样就破坏了js的函数式特点。

因为new是一个关键字，而不是一个函数。

new后面跟的是构造函数，而不是类的名字。

为了跟普通函数区别，构造函数的首字母是大写的。

构造函数使用的时候，如果前面不加new。

里面的this，就是指向了全局对象了。就有问题。





基于类和基于原型的继承的对比

| 基于类的继承                                     | 基于原型的继承       |
| ------------------------------------------------ | -------------------- |
| 类是不可变的，你无法在运行时修改或者添加新的方法 | 类是灵活的。         |
| 类可能不支持多重继承                             | 可以继承多个原型对象 |
| 比较复杂，你需要使用抽象类、接口等。             | 简洁。               |

new是js为了看起来跟java有点像，而加尽量的东西，是个历史遗留。

应该减少new的使用。



没有原型的时候，所有属性都单独有一份，而这是不必要的，而且带来了浪费。很多东西，多个对象之间是可以共用的。

为了解决这个问题，设计者为构造函数增加了一个属性：prototype。





# 理解原型继承

原型继承很简单。

你记住一点：只有对象，没有类。

有两种方式来创建一个对象：

```
1、无中生有。
	var obj = Object.create(null);
2、基于已有对象创建。
	var obj2 = Object.create(obj);
```





封装和继承



# 构造函数继承

有个动物对象的构造函数。

```
function Animal() {
	this.species = "动物"
}
```

还有一个猫对象的构造函数。

```
function Cat(name, color) {
	this.name = name;
	this.color = color;
}
```

怎么让猫继承动物呢？

有这些方法：

1、构造函数绑定

用apply或者call方法。

```
function Animal() {
    this.species = "animal"
}
function Cat(name, color) {
	Animal.apply(this, arguments)
    this.name = name;
    this.color = color;
}
var cat = new Cat("xx");
console.log(cat)
```

2、prototype模式

使用构造函数的prototype属性。这种方式更加常用。

让猫对象的prototype属性，指向一个Animal实例。

每一个prototype对象，都有一个constructor属性，指向构造函数。

```
function Animal() {
    this.species = "animal"
}
function Cat(name, color) {
    this.name = name;
    this.color = color;
}
Cat.prototype = new Animal()
Cat.prototype.constructor = Cat//这一行是必须的。不然默认是Animal。
var cat = new Cat("xx", "blue")
console.log(cat)
console.log(cat.species)
```

3、直接继承prototype

是指这个：

```
Cat.prototype = Animal.prototype;
```

这种方法是对方法2的改进。

但是也有点问题。所以有了方法4.

4、利用空对象作为中介。

```
var F = function() {}//F是空对象，占内存很少。
F.prototype = Animal.prototype
Cat.prototype = new F()
Cat.prototype.constructor = Cat
```

5、拷贝继承。



js只支持实现继承，无法实现接口继承。





this是什么？

为什么要用this？

先看一段代码。

```
function identify() {
	return this.name.toUpperCase();
}

function speak() {
	var greeting = "Hello, I'm " + identify.call( this );
	console.log( greeting );
}

var me = {
	name: "Kyle"
};

var you = {
	name: "Reader"
};

identify.call( me ); // KYLE
identify.call( you ); // READER

speak.call( me ); // Hello, I'm KYLE
speak.call( you ); // Hello, I'm READER
```

我们也可以选择不用this。而在函数的参数里，明确把参数传递进去。

```
var me = {
	name: "Kyle"
};

var you = {
	name: "Reader"
};

function identify(context) {
	return context.name.toUpperCase();
}

function speak(context) {
	var greeting = "Hello, I'm " + identify( context );
	console.log( greeting );
}

speak( you ); // READER
speak( me ); // Hello, I'm KYLE
```

这两种方式对比，我们就可以看到：

this机制提供了更优雅的方式，来隐式地传递一个对象的引用。

让代码更加干净，复用也更加容易。

当你的代码越复杂，你就越会感受到，明确传递对象影响，比this会显得更加混乱。

this到底指向的是谁？

有人认为this是指向函数自己。

为什么你想要在函数内部引用它自己 ？

下面代码在nodejs里运行。

```
global.count = 0;
function foo(num) {
	console.log( "foo: " + num );

	// 追踪 `foo` 被调用了多少次
	this.count++;
}

foo.count = 0;

var i;

for (i=0; i<10; i++) {
	if (i > 5) {
		foo( i );
	}
}
// foo: 6
// foo: 7
// foo: 8
// foo: 9

// `foo` 被调用了多少次？
console.log( foo.count ); // 0 -- 这他妈怎么回事……？
console.log(global.count)
```

this实际上是指向了函数调用者。

当前我们是在全局域调用了foo函数，所以在foo函数里，this就是global。





参考资料

1、一张图看透JavaScript原型关系：`__proto__`（对象原型）和prototype（函数原型）

https://blog.csdn.net/baidu_37107022/article/details/72461716

2、三分钟看完JavaScript原型与原型链

https://juejin.im/post/5a94c0de5188257a8929d837

3、如何理解JavaScript的原型和原型链？

http://web.jobbole.com/95606/

4、为什么原型继承很重要

https://segmentfault.com/a/1190000002596600

5、Javascript继承机制的设计思想

http://www.ruanyifeng.com/blog/2011/06/designing_ideas_of_inheritance_mechanism_in_javascript.html

6、你不懂JS: this 与对象原型

https://www.kancloud.cn/kancloud/you-dont-know-js-this-object-prototypes/516674