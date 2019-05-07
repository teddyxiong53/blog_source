---
title: js之escape和encodeURI区别
date: 2019-05-06 17:16:25
tags:
	- js
---



js里有3个函数可以对字符串进行编码：

1、escape。

2、encodeURI。

3、encodeURIComponent。

这3个函数有什么区别？

escape除了这些字符不转码，其余的都会转码。包括大于、小于这些都会被转码

```
a-z
A-Z
0-9
- _ . ! ~ * ' ( ) 
```

encodeURI

这个函数的目的是对URI进行完整的编码，下面这些特殊符号在URI里是有特殊意义的，所以不会被转码。

```
：;/?:@&=+$,#
```

encodeURIComponent

这个就是编码URI里的一部分，对特殊字符的处理有些不一样。

```
其他字符（比如 ：;/?:@&=+$,# 这些用于分隔 URI 组件的标点符号），都是由一个或多个十六进制的转义序列替换的。
```



结论：

1、不要用escape来对url编码。

2、



参考资料

1、escape()、encodeURI()、encodeURIComponent()区别详解

https://www.cnblogs.com/qiantuwuliang/archive/2009/07/19/1526687.html