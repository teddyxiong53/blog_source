---
title: nodejs之lodash
date: 2019-03-04 16:42:03
tags:
	- nodejs
---



看nodejs的底层库，看到很多都用到了lodash这个库。

这个库是做什么的呢？

lodash是一个js的原生库。

不需要引入其他依赖。

设计目的是：提高开发者效率，提高原生方法的性能。

lodash用一个下划线来表示，就像jquery用$来表示一样。这样用起来非常简洁。

可以在浏览器里使用，也可以在nodejs里使用。



常用lodash函数



不过到了ES6之后，很多东西语言本身已经带了。



引入lodash的方法

前端：

```
<script src="https://cdn.jsdelivr.net/npm/lodash@4.17.10/lodash.min.js"></script>
```

nodejs：

```
var _ = require("lodash")
```



可以被ES6语法取代的lodash功能有下面这些。

```
> [1,2,3].map(n=>n*2)
[ 2, 4, 6 ]
> [1,2,3].reduce((total,n)=>total+n)
6
> [1,2,3].filter(n=> n<=2)
[ 1, 2 ]
```

```
> const [head,...tail] = [1,2,3]
undefined
> head
1
> tail
[ 2, 3 ]
```



参考资料

1、lodash入门

https://www.jianshu.com/p/d46abfa4ddc9

2、

https://www.zhihu.com/topic/20029773/hot

3、可以使用ES6取代的10个Lodash特性

https://www.w3cplus.com/javascript/lodash-features-replace-es6.html