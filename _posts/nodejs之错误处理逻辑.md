---
title: nodejs之错误处理逻辑
date: 2020-08-28 21:22:08
tags:
	- nodejs

---

--

- [Error](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) object
- [Try…catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch)
- [Throw](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/throw)
- [Call stack](https://developer.mozilla.org/en-US/docs/Glossary/Call_stack)
- Effective [function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions) naming
- Asynchronous paradigms like [promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)



try catch默认是同步的。

在异步回调里throw，同步代码里是catch不到的。



参考资料

1、

https://stackify.com/node-js-error-handling/