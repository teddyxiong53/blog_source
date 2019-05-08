---
title: js之面向对象
date: 2019-03-16 14:12:11
tags:
	- js
---



# 对象的定义

对象是js里的一种基本数据类型，是一种符合之，它把多个值聚合在一起，可以通过名字来访问这些值。



# 对象的创建方法

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





创建对象的方法。



1、工厂模式。

```
function createPerson(name, age) {
    var o = new Object();
    o.name = name;
    o.age = age;
    o.sayName = function() {
        console.log(this.name);
    }
    return o;
}
var person1 = createPerson("xx", 10);
```

工厂方法虽然解决了创建多个相似对象的问题，但是没有解决如何识别对象类型的问题。

js经过发展，有了构造函数模式。

2、构造函数模式。

```
function Person(name, age) {
    this.name = name;
    this.name = age;
    this.sayName = function() {
        console.log(this.name);
    }
}
var person1 = new Person("xx", 10);
```

跟工厂模式的不同：

```
1、没有显式创建对象。
2、把属性都赋值给了this。
3、没有return。
```

一个匿名对象，会交给window对象接管。

```
Person("xx", 10);
window.sayName();//
```

构造函数模式，虽然有很大改进，但是还是有缺点，最主要就是函数成员。

这个可以提取出来的。

所以，就有了第三种模式。原型模式。

3、原型模式。

```
    <script>
        function Person() {

        }
        Person.prototype.name = "xx";
        Person.prototype.age = 10;
        Person.prototype.sayName = function() {
            console.log(this.name);
        };
        var person1 = new Person();
        var person2 = new Person();
        console.log(person1.sayName == person2.sayName);
    </script>
```



在实际使用中，我们是组合使用构造函数和原型模式。

```
function Person(name, age) {
            this.name = name;
            this.age = age;
        }
        Person.prototype = {
            constructor: Person,
            sayName: function() {
                console.log(this.name);
            }
        }
```

把函数提取到原型里。



1、js之对象（经典）

https://www.cnblogs.com/libin-1/p/5911190.html