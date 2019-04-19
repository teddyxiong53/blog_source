---
title: js之箭头函数
date: 2019-04-19 16:32:25
tags:
	- js

---



从直觉上看，箭头函数比普通函数要简洁一点。

除了这个，还有什么本质上的不同吗？

箭头函数不会改变this的绑定。默认绑定外层this。

我们看一个例子。

```
function Counter() {
    this.num = 0;
}
a = Counter();
console.log(a.num);
```

上面这样没有问题。

我们再继续加一点代码。

```
function Counter() {
    this.num = 0;
    this.timer = setInterval(function add() {
    	this.num ++;
    	console.log(this.num);
    },1000)
}
b = Counter();
```

我们的本意是希望，每1秒打印一下num，num不停自加。

但是实际上会报num这个找不到。

为什么？

因为setInterval这个函数是window对象的属性。

所以在这个函数里，this表示的就是window对象，而window对象没有num这个属性。

箭头函数可以解决这个问题。

```
function Counter() {
    this.num = 0;
    this.timer = setInterval(()=> {//就改这一行就好了。
    	this.num ++;
    	console.log(this.num);
    },1000)
}
b = Counter();
```









参考资料

1、

https://blog.fundebug.com/2017/05/24/arrow-function-for-beginner/

2、

https://juejin.im/post/5aa1eb056fb9a028b77a66fd