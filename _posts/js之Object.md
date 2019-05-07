---
title: js之Object
date: 2019-01-23 09:47:55
tags:
	- js

---



Object对象，是js里所有对象的基类。

Object.prototype定义了所有js对象的基本方法和属性。

```
构造函数
	new Object()
	new Object(value)//value可以是任意值，根据值的类型返回不同类型的对象。
	
```



```
prototype
	对象类的属性。
__proto__
	对象的属性。
对象的constructor等于类。所以obj.constructor.prototype等于类的原型。
```



一个类继承的示例。

```
<script >
        function People(name) {
            this.name = name;
        }
        function Student(age) {
            this.age = age;
        }
        Student.prototype = new People();
        var s = new Student(22);
        console.log(s.__proto__);
        console.log(Student.prototype);
        console.log(s.__proto__ == Student.prototype);//true
</script>
```



```
function People(name) {
this.name = name;
}
function Student(age) {
this.age = age;
}
Student.prototype = new People();
var s = new Student(22);
Student.prototype.sayHello = function() {
console.log("student say hello");
}
p = new People("xx");
s.sayHello();//ok
p.sayHello();//not ok
```



Object实例的方法

```
hasOwnPropter(name:string) 返回bool值
	判断一个类是否有自己的某个属性。继承的不算。
isPrototypeOf：判断某个原型是否出现在对象的原型链里。

```



Object的静态方法

```
Object.create(prototype, 属性描述符)
```

举例

```
<script >
        var obj = Object.create(null, {
            name: {
                value: 'allen',
                writable: true,
                enumerable: true,
                configurable: true
            },
            age: {
                value:22
            }
        });
    </script>
```



在node的repl里，输入Object，然后加上点号，按tab键补全，可以看到这些提示。

下面测试的基本数据是：

```
> obj = {a:1,b:2}
{ a: 1, b: 2 }
```



```
Object.__defineGetter__
Object.__defineSetter__
Object.__lookupGetter__
Object.__lookupSetter__
Object.__proto__
Object.hasOwnProperty
Object.isPrototypeOf
Object.propertyIsEnumerable
Object.toLocaleString
Object.valueOf
Object.apply
Object.arguments
Object.bind
Object.call
Object.caller
Object.constructor
Object.toString
Object.assign
	把多个对象的属性赋值到目标对象。
	返回值和目标对象的内容一样。
	> var ret = Object.assign(obj, {c:3,d:4})
    undefined
    > ret
    { a: 1, b: 2, c: 3, d: 4 }
    > obj
    { a: 1, b: 2, c: 3, d: 4 }
Object.create
	基于一个现有对象来创建一个新的对象。
	> obj1 = Object.create(obj)
    {}
    > obj1
    {}
    > obj1.a
    1
    > ojb1.b
    2
Object.defineProperties
Object.defineProperty
Object.entries
Object.freeze
Object.getOwnPropertyDescriptor
Object.getOwnPropertyDescriptors
Object.getOwnPropertyNames
Object.getOwnPropertySymbols
Object.getPrototypeOf
Object.is
Object.isExtensible
Object.isFrozen
Object.isSealed
Object.keys
Object.length
Object.name
Object.preventExtensions
Object.prototype
Object.seal
Object.setPrototypeOf
Object.values
```



而对obj，进行tab补全，就没有什么对象了，就是自己加进去的那些属性了。



参考资料

1、JavaScript Object对象

https://www.cnblogs.com/polk6/p/4340730.html