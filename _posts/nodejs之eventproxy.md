---
title: nodejs之eventproxy
date: 2019-08-22 15:22:03
tags:
	- nodejs
---



1

通过事件实现异步协作是eventproxy的主要亮点。

除此之外，它还是一个基本的事件库。

有这些基本的api

```
on/addListener：设置事件监听
emit：触发事件
once：on的特例，这种事件只发生一次。
removeListener：移除事件监听。
removeAllListeners：移除所有事件监听。
```

为了方便不同的库的使用习惯，给上面这些基本api设置了别名。

例如，对于jquery，把emit设置trigger别名。把on设置bind别名。

# 一个例子

下面的是之前的错误处理。是靠监听触发和监听error事件。

看起来不够简洁优雅。

```
var eventproxy = require('eventproxy')

function postProcess(error, content) {
    if(error) {
        console.log("error happens:", error)
    } else {
        console.log(content)
    }
}
function getContent(callback) {
    var ep = new eventproxy()
    ep.all('tpl', 'data', function(tpl, data) {
        callback(null, {
            template: tpl,
            data: data
        })
    })
    ep.bind('error', function(err) {
        ep.unbind()
        callback(err)
    })
    setTimeout(() => {
        ep.emit('tpl', 'aaa')
    }, 1000);
    setTimeout(()=> {
        var i = Math.random()*100
        console.log(i)
        if(parseInt(i)%2 == 0) {
            ep.emit('error', 'ccc')
        }
        ep.emit('data', "bbb")
    }, 2000)

}

getContent(postProcess)
```

经过实践总结，得到下面更好的方式。

```
function getContent(callback) {
    var ep = new eventproxy()
    ep.all('tpl', 'data', function(tpl, data) {
        callback(null, {
            template: tpl,
            data: data
        })
    })
    ep.fail(callback)//添加错误处理

    setTimeout(ep.done('tpl'), 1000);
    setTimeout(ep.done('data'),1000);
}
```

不同在于，使用ep.fail来处理出错。

把ep.done直接作为回调。

在done的内部，就已经处理了error的情况，在出错的时候，emit一个error事件。

```
  EventProxy.prototype.done = function (handler, callback) {
    var that = this;
    return function (err, data) {
      if (err) {
        // put all arguments to the error handler
        return that.emit.apply(that, ['error'].concat(SLICE.call(arguments)));
      }

```

```
fs.readFile('1.txt', ep.done('content'))
```

等价于

```
fs.readFile('1.txt', function(err, content) {
	if(err) {
		return ep.emit('error', err)
	}
	ep.emit('content', content)
})
```

done的内部，已经封装了error-first参数。



代码在这里。

https://github.com/JacksonTian/eventproxy

# 自己实现

实现一个最简单的版本。来帮助理解和分析。

myeventproxy.js

```
'use strict'

var SLICE = Array.prototype.slice
var CONCAT = Array.prototype.concat

var ALL_EVENT = '__all__'

var EventProxy = function() {
    if(!this instanceof EventProxy) {
        return new EventProxy()
    }
    this._callbacks = {}
    this._fired = {}
    console.log('eventproxy created')
}

EventProxy.prototype.addListener = function(ev, callback) {
    this._callbacks[ev] = this._callbacks[ev] || []
    this._callbacks[ev].push(callback)
    return this
}
EventProxy.prototype.on = EventProxy.prototype.addListener

/*
    因为一个eventname下面，挂的callback，是一个数组，所以需要指定移除某一个callback。
    如果不指定callback，则把eventname下面所有的callback都移除。
    如果不指定eventname，那么把所有的callback都移除。
*/
EventProxy.prototype.removeListener = function(eventname, callback) {
    var calls = this._callbacks
    if(!eventname) {
        console.log('remove all listeners')
        this._callbacks = {}
    } else {
        if(!callback) {
            console.log('remove all listeners of ', eventname)
            callback[eventname] = []
        } else {
            var list = calls[eventname]
            if(list) {
                var l = list.length
                for(let i=0; i<l ;i++) {
                    if(callback == list[i]) {
                        console.log("remove a listener of ", eventname)
                        list[i] = null
                    }
                }
            }
        }
    }
    return this
}

EventProxy.prototype.emit = function(eventname, data) {
    var both = 2//为什么是2
    var list, ev, callback, i, l
    var calls = this._callbacks
    while(both --) {
        //如果both不为0，那么就
        ev = both? eventname: ALL_EVENT
        console.log('ev:',ev)
        list = calls[ev]
        if(list) {
            for(i=0, l=list.length; i<l; i++) {
                callback = list[i]
                if(!callback) {//对应的回调是空的。从数组里清除掉。
                    list.splice(i,1)
                    i--
                    l--
                } else {
                    var args = []
                    var start = both ? 1 : 0
                    for(var j=start; j<arguments.length; j++) {
                        args.push(arguments[j])
                    }
                    callback.apply(this, args)
                }
            }
        }
    }
    return this
}

module.exports = EventProxy
```

测试

```
var EventProxy = require('./myeventproxy')

var proxy = new EventProxy()

proxy.on('aaa', function(x, y,z) {
  console.log('aaa happen')
  console.log(x, y, z)
})

proxy.emit('aaa', 1,2,3)
console.log('end')
```

输出：

```
eventproxy created
ev: aaa
aaa happen
1 2 3
ev: __all__
end
```

emit的时候，是直接把回调函数自己调用执行了。

on和emit是一起的。

bind和unbind是一起。





eventproxy的替代

应该用await异步来可以替代。



参考资料

1、使用 eventproxy 控制并发

http://wiki.jikexueyuan.com/project/node-lessons/eventproxy.html