---
title: js之正则表达式
date: 2019-05-07 09:51:25
tags:
	- js
---



js的正则表达式是参考perl5的建立的。

新建一个正则表达式有两种方法：

```
var regex = /xyz/; //用/开始，用/结束。字面常量的方式。
```

```
var regex = new RegExp('xyz');//构造函数的方式。
```

这两种方式的区别的是：

字面常量的方式，在编译时就生效了。

而构造函数的方式，则在运行时才生效。

而且字面常量的方式，看起来更加直观，所以我们一般都使用字面常量的方式。



属性有：

```
ignoreCase
global
multiline
```

例子：

```
> var r = /agc/igm
undefined
> r.flags
'gim'
```

# 方法

## test

```
> /cat/.test("cat and dog")
true
```

加上g属性后，每次都是从上次的位置继续往后找的。

```
> var r= /x/g
undefined
> var s = "_x_x"
undefined
> r.lastIndex
0
> r.test(s)
true
> r.lastIndex
2
> r.test(s)
true
> r.lastIndex
4
> r.test(s)
false
```

我们可以通过修改lastIndex，来告诉正则表达式从哪里开始匹配。

## exec

返回的是数组。

```
var s = '_x_x';
var r1 = /x/;
var r2 = /y/;

r1.exec(s) // ["x"]
r2.exec(s) // null
```





参考资料

1、RegExp 对象

https://wangdoc.com/javascript/stdlib/regexp.html

2、

https://www.jb51.net/article/84784.htm

3、

https://blog.csdn.net/weixin_42142603/article/details/114646470

4、

https://blog.csdn.net/yzbben/article/details/53467659

5、

https://stackoverflow.com/questions/494035/how-do-you-use-a-variable-in-a-regular-expression