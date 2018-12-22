---
title: js之对象
date: 2018-12-22 14:00:17
tags:
	- js
---





#对象的定义

对象是js里的一种基本数据类型，是一种符合之，它把多个值聚合在一起，可以通过名字来访问这些值。



#对象的创建方法

1、直接创建。

```
var obj = {
    name : "xx",
    age: 10
};
console.log(obj.name);
```

2、用构造函数。

系统自带的Object、Array、Number、Boolean、Date这些。

```
var obj = new Object();
obj.name = "xxx";
```

自定义的构造函数，注意，也是用function来定义。和普通函数，就是命名上做区分。这个首字母大写。

```
function Obj(name) {
    this.name = name;
    this.age = 18;
}
var obj = new Obj('xx');
```

自定义构造函数的基本原理：

关键在于new这个操作符。

不用new的话，就没有返回值，跟普通函数一样执行了。

有了new，就会返回一个对象了。



# 对象的增删改查

增

就是直接给一个新的属性赋值就好了。访问没有的属性只会提示undefined。

```
var obj = {};
console.log(obj.name);
obj.name = "xx";
```

删

可以删除属性。用delete就可以。

```
var obj = {
name: "xx"
};
console.log(obj.name);
delete obj.name;
console.log(obj.name);
```

改

很简单，重新赋值就好了。

查

有两种方法，一种就是用点号了。一种用['name']这种方式。



# 原型

原型是function对象的一个属性。

它定义了构造函数生成的对象的公共祖先。

原型也是对象。

利用原型，可以提取公共属性，放在原型里，这样就不用每次都重新定义一遍所有的属性了。

举例如下：

```
Person.prototype = {
eat: function (food) {
console.log("eat " + food);
},
sleep:function() {
console.log("I am sleeping");
}
}
function Person(name, age) {
this.name = name;
this.age = age;
}
var p1 = new Person("xx", 18);
p1.eat("apple");
```



# 参考资料

1、js之对象（经典）

https://www.cnblogs.com/libin-1/p/5911190.html