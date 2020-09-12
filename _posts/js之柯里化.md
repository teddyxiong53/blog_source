---
title: js之柯里化
date: 2020-09-09 11:25:17
tags:
	- js

---

1

看介绍lodash的文章，里面提到：

Fixed Arity，固化参数个数，便于柯里化

什么是柯里化？

**Currying** 为实现多参函数提供了一个递归降解的实现思路——**把接受多个参数的函数变换成接受一个单一参数（最初函数的第一个参数）的函数，**

**并且返回接受余下的参数而且返回结果的新函数**，

在某些编程语言中（如 Haskell），是通过 **Currying** 技术支持多参函数这一语言特性的。

所以 **Currying** 原本是一门编译原理层面的技术，用途是**实现多参函数**。

所以 **Currying** 是应函数式编程而生，在有了 **Currying** 后，大家再去探索去发掘了它的用途及意义。 然后因为这些用途和意义，大家才积极地将它扩展到其他编程语言中



我们写一个简单的add函数，把它柯里化看看。

```js
function add(x, y) {
    return (x+y)
}
```

实现柯里化，用法是这样的：

```
curriedAdd(1)(3) //结果是4
```

实现是这样：

```
function curriedAdd(x) {
	return function(y) {
		return x+y
	}
}
```

上面这个实现是有问题的。

它并不通用，而且重新编码来实现柯里化，也是一个比较麻烦的事情。

但是这个 `curriedAdd` 的实现表明了实现 **Currying** 的一个基础 —— **Currying** 延迟求值的特性需要用到 JavaScript 中的作用域——说得更通俗一些，我们需要使用作用域来保存上一次传进来的参数。

```
function trueCurrying(fn, ...args) {
    if (args.length >= fn.length) {
        return fn(...args)
    }
    return function (...args2) {

        return trueCurrying(fn, ...args, ...args2)
    }
}
```

以上函数很简短，但是已经实现 **Currying** 的核心思想了。JavaScript 中的常用库 Lodash 中的 curry 方法，其核心思想和以上并没有太大差异

Lodash 中实现 **Currying** 的代码段较长，因为它考虑了更多的事情，比如绑定 this 变量等。



参考资料

1、大佬，JavaScript 柯里化，了解一下？

https://juejin.im/post/6844903603266650125