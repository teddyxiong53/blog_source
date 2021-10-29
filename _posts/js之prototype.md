---
title: js之prototype
date: 2019-01-23 09:18:55
tags:
	- js

---



对于java开发人员来说，js有点让人困惑，因为它是动态的，而且本身不提供class实现。

在ES6里，引入了class关键字，但是只是语法糖，js仍然是基于原型的。

js通过函数来模拟类。

当谈到继承时，js只有一种结构：对象。

每个对象都有一个私有属性`__proto__`，指向自己的原型对象。

原型对象也有自己的`__proto__`，这样层层往上，最上层的这个属性是null。

根据定义，null没有原型，作为原型链的最后一环。

尽管这种原型链继承被认为是js的弱点，但是实际上原型链继承比经典模型更加强大。

```
<script >
        let f = function() {
            this.a = 1;
            this.b = 2;
        }
        var o = new f();
        f.prototype.b = 3;
        f.prototype.c = 4;
        console.log("o.a:", o.a);
        console.log("o.b:", o.b);
        console.log("o.c:", o.c);
        console.log("o.d:", o.d);
</script>
```



只有函数才有prototype属性。

当你创建一个函数的时候，js自动为这个函数添加prototype属性。



js是单继承的。



在ES5里，加入了Object.create这种创建对象的方法。

在ES6里，加入了class、extends、super、static这些关键字。

看起来更加像类了。

示例：

```
<script >
        class Book {
            constructor(props) {
                this._title = props.title;
            }
            get title() {
                return this._title;
            }
            static staticMethod() {

            }
            toString() {
                return `book_${this._title}`;
            }
        }
        class EBook extends Book {
            constructor(props) {
                super(props);
                this._link = props.link;
            }
            set link(val) {
                this._link = val;
            }
            toString() {
                return `book_${this._link}`;
            }
        }
        var book1 = new EBook({title:"book1", link:"link1"});
        var info = "info: " + book1;
        console.log(info);
</script>
```





JavaScript对每个创建的对象都会设置一个原型，指向它的原型对象。

当我们用`obj.xxx`访问一个对象的属性时，**JavaScript引擎先在当前对象上查找该属性，如果没有找到，就到其原型对象上找，如果还没有找到，就一直上溯到`Object.prototype`对象，最后，如果还没有找到，就只能返回`undefined`。**

例如，创建一个`Array`对象：

```
var arr = [1, 2, 3];
```

其原型链是：

```
arr ----> Array.prototype ----> Object.prototype ----> null
```

`Array.prototype`定义了`indexOf()`、`shift()`等方法，因此你可以在所有的`Array`对象上直接调用这些方法。

当我们创建一个函数时：

```
function foo() {
    return 0;
}
```

函数也是一个对象，它的原型链是：

```
foo ----> Function.prototype ----> Object.prototype ----> null
```



参考资料

1、继承与原型链

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Inheritance_and_the_prototype_chain

2、从`__proto__`和prototype来深入理解JS对象和原型链 

https://github.com/creeperyang/blog/issues/9

3、JavaScript中的“多继承”

https://zhuanlan.zhihu.com/p/34693209

4、Javascript继承机制的设计思想

http://www.ruanyifeng.com/blog/2011/06/designing_ideas_of_inheritance_mechanism_in_javascript.html

5、

https://www.liaoxuefeng.com/wiki/1022910821149312/1023022043494624