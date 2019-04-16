---
title: js之链式调用
date: 2019-04-16 09:50:28
tags:
	 - js
---



链式调用优点是可以减少代码量，缺点是会占用返回值。

链式调用，跟builder模式是一起的。

特点就是所调用的函数的返回值都是this。

举例：

```
function ClassA() {
    this.prop1 = null;
    this.prop2 = null;
    this.prop3 = null;
}

ClassA.prototype = {
    method1: function(p1) {
        this.prop1 = p1;
        return this;
    },
    method2: function(p2) {
        this.prop2 = p2;
        return this;
    },
    method3: function(p3){
        this.prop3 = p3;
        return this;
    },

};

var obj = new ClassA();
obj.method1(1).method(2).method3(3);
```



参考资料

1、javascript链式调用实现方式总结

https://www.cnblogs.com/youxin/p/3410185.html