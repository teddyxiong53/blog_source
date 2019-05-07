---
title: js之typeof和instanceof区别
date: 2019-05-07 11:03:25
tags:
	- js
---



我在测试js的api的时候，发现这个：

```
> 'a' instanceof String
false
> typeof 'a'
'string'
```

为什么不是？

typeof会返回一个变量的基本类型。

基本类型包括：

```
number
string
object
boolean
function
undefined
```

typeof对数组、null、对象，都会返回object。

判断不够精确，所以需要instanceof来帮助我们准确判断。



参考资料

1、js中typeof和instanceof用法区别

https://blog.csdn.net/qq_27626333/article/details/76146078