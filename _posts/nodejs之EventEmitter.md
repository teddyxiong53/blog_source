---
title: nodejs之EventEmitter
date: 2018-12-22 14:42:17
tags:
	- nodejs
---





nodejs所有异步io操作都会在完成时，发送一个事件到事件队列。

nodejs里许多对象都会分发事件。

例如：net.Server对象会在每次有连接的时候触发一个事件。

一个fs.readStream对象会在文件被打开的时候触发一个事件。



所有会产生事件的对象都是events.EventEmitter的实例。

新建test.js。

```
var EventEmitter = require("events");
var event = new EventEmitter();
event.on("some_event", function() {
	console.log("some_event happens");
});

setTimeout(function() {
	event.emit("some_event");
}, 1000);
```

node test.js。执行可以看到效果。



大多数时候，我们都是继承EventEmitter，而不是直接使用它。



参考资料

1、Node.js EventEmitter

http://www.runoob.com/nodejs/nodejs-event.html

















