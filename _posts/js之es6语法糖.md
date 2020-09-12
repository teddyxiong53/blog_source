---
title: js之es6语法糖
date: 2019-05-08 14:20:28
tags:
	- js

---

1

ES6为一些已有的功能**提供了非破坏性的更新。**

这种更新，大部分我们可以理解为语法糖。

所谓语法糖，就是这些东西，用ES5完全也可以做到，但是ES6帮我们简化了一下，写起来更简单直观一些。

# 对象字面量

对象字面量是指以{}形式直接表示的对象。

例如这样：

```
var book = {
	title: "xx",
	author: "yy"
}
```

ES6针对这个的改进有：

1、属性的简洁表示法。

2、可计算的属性名。

## 属性的简洁表示法

很多时候，属性的key和value，都是一样的。

```
var title = "xx"
var book = {
	title: title
}
```

这个可以简写成这样：

```
var book = {
	title
}
```

在不影响语义的前提下，减少了冗余代码。

## 可计算的属性名

```
var read = 'news'
var person = {
    name: "xx",
    [read] : ['sport', 'money']
}
console.log(person)
```

需要用中括号括起来。中括号里，可以是一个表达式。

注意，属性简洁表示法和可计算的属性名这2个特性，不能同时使用。

会报错的。

可计算属性名是个很有用的特性。

可以让我们的代码显得更加简洁。

## 新对象的属性引用自另外一个对象

```
var student = {
    name: 'xx',
    age: 10
}

var students = {
    [student.name]: student
}

console.log(students)
```

### 方法定义

以前，要这么写。

```
var student = {
    name: 'xx',
    age: 10,
    study: function () {
        console.log("study")
    }
}
```

现在可以这么写：

```
var student = {
    name: 'xx',
    age: 10,
    study() {
        console.log("study")
    }
}
```

省去了function关键字和冒号。

# 箭头函数

js里，普通函数：

```
function name(parameters) {
	//body
}
```

一般包括函数名、参数、函数体。

普通匿名函数：

```
var func = function(parameters) {
	//body
}
```

没有函数名。一般是赋值给了一个变量。

或者是直接调用了。

箭头函数：

```
var func = (parameters) => {
	//body
}
```

省掉了function关键字，没有函数名。

看起来，有点像匿名函数，但是他们有很大的本质不同。

```
1、箭头函数不能被直接命名，但是可以被赋值给一个对象。
2、箭头函数不能做构造函数。所以不能在前面加new。
3、箭头函数没有prototype属性。
4、绑定了词法作用域，不会修改this的指向。
```

箭头函数的作用域，用apply、call、bind都无法改变的。

箭头函数没有arguments属性。



## 箭头函数的简写

只有一个参数时，可以省掉参数的小括号。

```
var double = value => {
	return value*2;
}
```

如果函数体很简单，而且可以一行写完。大括号也可以省掉。

```
var double = value => value*2;
```

## 箭头函数注意事项

如果你的箭头函数返回的是一个对象，要在大括号外面包小括号。

```
var xx = () => ({name: "xx"})
```

如果没有外面的小括号，大括号会被认为的函数体的。

# 解构赋值

ES6里最灵活的和富于表现性的特性。

先看一个例子。

```
var student = {
    name: 'xx',
    age: 10,
    study() {
        console.log("study")
    }
}
var name = student.name
var age = student.age
```

上面是ES5的语法，我们要拿到student的name属性。是这操作。

在ES6里，我们可以这样：

```
var {name, age} = student
```



# 剩余参数和拓展符

在ES6之前，对于不确定参数个数的函数。

我们需要使用伪数组arguments。

然后用Array.prototype.slice.call转化arguments为真数组后再操作。

```
function join() {
    var list = Array.prototype.slice.call(arguments)
    return list.join("--")
}
console.log(join("aa", "bb", "cc"))//aa--bb--cc
```

对于这种需求，ES6提供了更好的解决方案。

就是剩余参数，用3个点表示。

```
function join(...list) {
    return list.join("--")
}
console.log(join("aa", "bb", "cc"))
```

还可以这样：

```
function join(sep, ...list) {
    return list.join(sep)
}
console.log(join("--","aa", "bb", "cc"))
```



# 模板字符串

模板字符串是对js字符串的重大改进。

主要用途：

```
1、字符串内部计算。
2、多行文本。
	尤其对于html字符串很方便。
```



参考资料

1、重新认识ES6中的语法糖

https://segmentfault.com/a/1190000010159725