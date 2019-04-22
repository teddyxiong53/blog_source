---
title: 小程序之使用async
date: 2019-04-20 17:37:25
tags:
	- 小程序

---





小程序本身不支持async？为什么？

因为async和await是ES7的语法，小程序里的解释器，还只能支持ES6。

所以，只能通过引入第三方库来支持。

Facebook的regenerator就是一个很好的库。

我们只需要把regenerator-runtime目录下的runtime.js，放到我们小程序的utils目录或者lib目录下就好了。



async：定义异步函数。

```
1、自动把函数转换为Promise。
2、内部可以使用await。
3、这个函数被调用的时候，函数返回值会被resolve处理。
```



await：暂停异步函数的执行。

```
1、当使用在Promise的前面时，await等待Promise完成。并返回Promise的结果。
2、await只能跟Promise一起用，不能跟callback一起用。
```



使用的时候：

```
import 
```



https://github.com/facebook/regenerator

参考资料

1、小程序使用 async await

https://juejin.im/post/5c14b253e51d452f8e603896

2、让小程序支持async-await

https://segmentfault.com/a/1190000015691620