---
title: js之polyfill
date: 2020-09-10 10:24:17
tags:
	- js

---

1

Polyfill你可以理解为“腻子”，就是装修的时候，可以把缺损的地方填充抹平。

举个例子，html5的storage(session,local), 不同浏览器，不同版本，有些支持，有些不支持。

我们又想使用这个特性，怎么办？

有些人就写对应的Polyfill（Polyfill有很多），帮你把这些差异化抹平，不支持的变得支持了

你只需要把需要的Polyfill引入到你的程序里，就可以了。

举个例子，有些旧浏览器不支持Number.isNaN方法，Polyfill就可以是这样的：

```js
if(!Number.isNaN) 
{ 
    Number.isNaN = function(num) 
    { 
        return(num !== num);
    }
} 
```



啥意思呢，就是假如浏览器没有Number.isNaN方法，那咱们就给它添加上去，所谓Polyfill就是这样解决API的兼容问题的。



参考资料

1、polyfill为何物

https://juejin.im/post/6844903549768302606