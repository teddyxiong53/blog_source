---
title: js之基本对象Function
date: 2019-05-07 13:21:17
tags:
	- js
---

1

在node的repl里，输入Function，加上点，再按tab补全，得到这些内容：

```
Function.__defineGetter__
Function.__defineSetter__
Function.__lookupGetter__
Function.__lookupSetter__
Function.__proto__
Function.hasOwnProperty
Function.isPrototypeOf
Function.propertyIsEnumerable
Function.toLocaleString
Function.valueOf
Function.apply
Function.arguments
Function.bind
Function.call
Function.caller
Function.constructor
Function.toString
Function.length
Function.name
Function.prototype
```

func加点tab补全出来的内容，跟Function的一样。

```
> var func = new Function("a", "b", "return a+b")
> func(1,2)
3
```

加上打印参数的。

```
> var func = new Function("a", "b", "console.log(a,b);return a+b")
undefined
> func(1,2)
1 2
3
```

