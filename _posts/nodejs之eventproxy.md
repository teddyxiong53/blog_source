---
title: nodejs之eventproxy
date: 2019-08-22 15:22:03
tags:
	- nodejs
---



1

代码在这里。

https://github.com/JacksonTian/eventproxy

自己写测试代码。

```
var EventProxy = require("./lib/eventproxy")
var sleep = require("sleep")
var counter = 0
var ep = EventProxy.create('xhl-event', function(data) {
    sleep.sleep(1)
    counter += 1
    console.log(data)
})
ep.emit('xhl-event','xhl-data')
console.log("end")
```

输出是这样：

```
xhl-data
end
```

所以这个是同步执行的特点。



使用bind和trigger

```
var EventProxy = require("./lib/eventproxy")
var sleep = require("sleep")
var counter = 0

var ep = EventProxy.create()
ep.bind("xhl-event", function(data) {
    console.log(data)
    counter += 1
})
ep.trigger("xhl-event", "xhl-data1")
ep.trigger("xhl-event", "xhl-data2")
console.log("counter=" + counter)
```

还可以unbind，unbind之后，trigger就没有用了。可以对一个event bind多个处理函数。

还可以removeAllListeners。这个跟unbind效果类似。

```
ep.removeAllListeners("xhl-event")
```

headbind。是放到最前面处理。

once。特点是绑定的函数只能被执行一次。本质上是在执行后，内部进行了unbind操作。

immediate。这个是表示绑定的时候，马上触发一次。

assign。这个比较复杂。

after。在触发几次后执行函数。

any。注册多个事件，任意一个发生了就触发函数调用。

not。除了指定的这个事件外，其余事件都会触发。

done。执行回调后，执行指定的函数。

```
var done_func = function(num) {
	//
}
ep.bind("xhl-event", ep.done(done_func))
//ep.done(arg) arg还可以是另外一个事件。
```

fail。就是在on error的时候执行。



代码并不多，600行左右。

bind这些函数，本质都是addListener。

```
 EventProxy.prototype.bind = EventProxy.prototype.addListener;
 
 EventProxy.prototype.unbind = EventProxy.prototype.removeListener;
 
 EventProxy.prototype.emit = EventProxy.prototype.trigger;
 EventProxy.prototype.fire = EventProxy.prototype.trigger;
```





参考资料

1、

