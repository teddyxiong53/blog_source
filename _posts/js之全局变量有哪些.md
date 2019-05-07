---
title: js之全局变量有哪些
date: 2018-12-27 10:09:27
tags:
	- js
---



# 全局属性

```
Infinity
	表示正无穷大。
NaN
	不是数值。
	类型还是number类型的。
undefined
	
```

# 全局函数

```
decodeURI
encodeURI
escape
eval
isFinite
Number
	把对象的值转成数字。
parseFloat
parseInt
String
	把对象转成字符串。
unescape
	跟escape相反。
```

```
> Number({a:1})
NaN
> Number("123")
123
```



## decodeURI

```
参数：
	uri
返回：
	字符串
举例：
> encodeURI("www.baidu.com/你好")
'www.baidu.com/%E4%BD%A0%E5%A5%BD'
> var ret = encodeURI("www.baidu.com/你好")
undefined
> decodeURI(ret)
'www.baidu.com/你好'
```

## encodeURI

见上面例子。





参考资料

1、

https://blog.csdn.net/chenchunlin526/article/details/78908592

2、JavaScript 全局

https://www.runoob.com/jsref/jsref-obj-global.html