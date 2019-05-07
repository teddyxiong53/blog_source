---
title: js之基本对象Function
date: 2019-05-07 13:21:17
tags:
	- js
---

1

基本使用

```
> var err= new Error("xxx")
undefined
> err
Error: xxx
    at repl:1:10
    at Script.runInThisContext (vm.js:96:20)
    at REPLServer.defaultEval (repl.js:329:29)
    at bound (domain.js:396:14)
    at REPLServer.runBound [as eval] (domain.js:409:12)
    at REPLServer.onLine (repl.js:642:10)
    at REPLServer.emit (events.js:187:15)
    at REPLServer.EventEmitter.emit (domain.js:442:20)
    at REPLServer.Interface._onLine (readline.js:290:10)
    at REPLServer.Interface._line (readline.js:638:8)
```

```
> throw new Error("yy")
Error: yy
```

错误分类

```
EvalError
	eval函数里的错误。
InternalError
	表示js引擎内部的错误，例如递归层次太深。
RangeError
	超出范围。
ReferenceError
	无效引用。
SyntaxError
	语法错误。
TypeError
	类型错误。
URIError
	给encodeURI传递的参数有错误。
```

自定义错误类型

```
function MyError(message) {
    this.name = "MyError"
    this.message = message || "default message"
    this.stack = (new Error()).stack
}
MyError.prototype = Object.create(Error.prototype)
MyError.prototype.constructor = MyError
try {
    throw new MyError("xx")
} catch(e) {
    console.log("e.name", e.name);
    console.log("e.message", e.message)
    console.log("e.stack", e.stack)
}
```

参考资料

1、

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Error