---
title: js之this-instanceof-XX
date: 2021-10-27 13:31:33
tags:
	- nodejs

---

--

经常可以看到这种用法，

```
var EventProxy = function() {
    if(!this instanceof EventProxy) {//-------这里
        return new EventProxy()
    }
    this._callbacks = {}
    this._fired = {}
    console.log('eventproxy created')
}
```

为什么要这样判断一下？

作用是什么？

因为外面可能这样来调用：

```
var ep = EventProxy()
```

这样可以确保

```
var ep = EventProxy()
等价于
var ep = new EventProxy()
```

确保了this是EventProxy，而不是window等其他的东西。



参考资料

1、

https://stackoverflow.com/questions/22211755/function-f-if-this-instanceof-f-return-new-f