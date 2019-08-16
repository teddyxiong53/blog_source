---
title: js之类方法、对象方法和原型方法区别
date: 2019-08-16 15:37:36
tags:
	- nodejs

---

1

看下面的例子就全明白了。

```
function People(name) {
    this.name = name;
    this.sayName = function() {//这个就是对象方法
        console.log("my name is " + this.name);
    }
}
People.run = function() {
    console.log("I can run");
}

People.prototype.jump = function() {
    console.log("I can jump");
}

var p1 = new People("teddy");
p1.sayName();
//p1.run();//错误，类方法只能通过类名来使用。
People.run();
p1.jump();//主要原型方法也只能通过对象来使用。
```



参考资料

1、浅谈JS中 【类方法】【对象方法】【原型方法】

https://blog.csdn.net/aa294194253/article/details/42966161