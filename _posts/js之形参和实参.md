---
title: js之形参和实参
date: 2020-12-29 13:27:17
tags:
	- js

---

1

我看有的js的函数，形参没有写，但是实际上有可以传递参数进去。

实际传递进去的参数，可以通过arguments来拿到。

这个该怎么理解？

在JavaScript中`实参`与`形参`数量并不需要像JAVA一样必须在数量上严格保持一致，具有很大的灵活性。



如果一个函数中没有使用return语句，则它默认返回`undefined`。要想返回一个特定的值，则函数必须使用 `return` 语句来指定一个要返回的值。

如果实参是一个包含原始值(数字，字符串，布尔值)的变量，则就算函数在内部改变了对应形参的值，返回后，该实参变量的值也不会改变。

如果实参是一个对象引用，则对应形参会和该实参指向同一个对象。



参考资料

1、

