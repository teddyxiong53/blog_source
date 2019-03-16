---
title: js之面向对象
date: 2019-03-16 14:12:11
tags:
	- js
---





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

