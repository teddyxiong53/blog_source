---
title: js之变量解构赋值
date: 2019-03-15 15:11:11
tags:
	- js

---





这个是从ES6开始引入的语法。

它提供了一种途径：让我们可以方便地把采用从数组中，把属性从对象中提取出来并赋值给变量。

举例：

```
[a, b] = [10, 20] //结果就是a被赋值为10，b被赋值为20
[a, b, ...rest] = [1,2,3,4,5] //reset会得到剩下的3,4,5 。主要三个点的用法。
```



参考资料

1、解构赋值

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment

