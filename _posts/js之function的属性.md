---
title: js之function的属性
date: 2019-04-16 10:45:28
tags:
	 - js
---



通过vscode里的代码调整功能，在lib.es5.d.ts里，看到Function这个接口的定义是这样：

```
interface Function {
    apply(this, thisArg, argArray);
    call(this, thisArg, argArray);
    bind(this, thisArg, argArray);
    toString();

    prototype;
    length;
    arguments;
    caller: Function;
};
```

4个方法，4个属性。



apply、call。都是为了改变某个函数运行时的上下文而设计的。

简单说，就是改变函数内部的this的指向。

先看一个例子。

```
function fruits() {

}

fruits.prototype = {
    color: "red",
    say: function() {
        console.log("my color is :" + this.color);
    }
}

var apple = new fruits;
apple.say();
```

如果我们有一个对象banana，但是我们不想对它重新定义say方法，我们可以借用apple的say方法。

如下：

```
banana = {
    color: "yellow"
}

apple.say.call(banana);
apple.say.apply(banana);
```

使用场景就是：我们当前的对象没有某个方法，而其他对象有某个方法。我们可以借用其他对象的方法为我所用。

apply和call作用完全一样，区别就是接收参数的方法不同。

如下：

```
func.call(this, arg1, arg2);
func.apply(this,[arg1, arg2]);
```



常见的用法有

数组之间追加

```
var array1 = [12, "foo", {name: "xx"}, -1];
var array2 = ["yy", 55];
Array.prototype.push.apply(array1, array2);
作用就是array1变成了array1和array2拼起来的效果。
```

获取数组里的最大值和最小值

```
var numbers = [1, 20, 3, 5];
var maxInNumbers = Math.max.apply(Math, numbers);
```

数组没有max方法，但是Math有，我们可以这样来借用。



类数组或者伪数组使用数组方法

```
var domNodes = Array.prototype.slice.call(document.getElementsByTagName("*"));
```



有时候，我们会封装console.log函数。

例如这样：

```
function mylog(p) {
    console.log(p);
}

mylog(1);
mylog(1,2);
```

当参数个数不匹配的时候，就不符合我们的预期了，怎么办呢？

用apply可以搞定。

```
function mylog() {
    console.log.apply(console, arguments);
}
```

一般给消息加上独特的标志，也是一个常见的需求，怎么做到呢？

```
function mylog() {
    var args = Array.prototype.slice.call(arguments);
    args.unshift('(app)');
    console.log.apply(console, args);
}
```



下面我们继续看bind。

bind方法跟apply和call作用很相似，也是用来改变函数内部的this的指向。

bind方法会常见一个新的函数，称为绑定函数。

当调用这个绑定函数的时候，绑定函数会以bind创建时传递进去的第一个参数作为this。



在常见的单体模式里，我们通过会用_this、that、self来保存this，这样我们就可以在改变了上下文之后继续使用它。

```
var foo = {
    bar: 1,
    eventBind: function() {
        var _this = this;
        $('.someClass').on('click', function(event) {
            console.log(_this.bar);
        });
    }
}
```

由于js特有的机制，上下文环境在`eventBind: function()`过度到`$('.someClass').on('click'`时发生了变化。

我们用_this来做，也没有问题。

但是用bind，我们可以做得更加优雅。

```
var foo = {
    bar: 1,
    eventBind: function() {
        $('.someClass').on('click', function(event) {
            console.log(this.bar);
        }.bind(this));
    }
}
```



参考资料

1、深入浅出 妙用Javascript中apply、call、bind

https://www.cnblogs.com/coco1s/p/4833199.html