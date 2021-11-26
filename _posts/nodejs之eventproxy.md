---
title: nodejs之eventproxy
date: 2019-08-22 15:22:03
tags:
	- nodejs
---



1

eventproxy是一个很轻量的工具。

可以带来一种事件式编程的思维变化。

有几个特点：

1、利用事件机制解耦复杂业务逻辑。

2、解决回调嵌套问题。

3、把串行等待变成并行等待。提升多异步协作场景下的执行效率。

4、友好的error handling。

5、无平台依赖。



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

# 异步场景使用

## 多类型异步

例如，页面渲染的情况。

需要获取模板、数据。都是异步的获取的。

用ep.all在最后来组合处理前面多个异步的内容。

那么这样写。

```
var ep = new EventProxy()
ep.all('tpl', 'data', function(tpl, data) {
	//最后的处理
})
fs.readFile('template.tpl', function(err, content) {
	ep.emit('tpl', content)
})
db.get('some sql ', function(err, result) {
ep.emit('data', result)
})
```

all的回调函数的参数，是以事件的返回内容为顺序的。

例如，按照tpl和data的顺序来注册的，那么回调函数的第一个参数就是tpl事件返回的数据。以此类推。

几种等价写法

```
ep.all('aa', bb', function(){})
等价于
ep.all(['aa', 'bb'], function(){})
```

```
var ep = EventProxy('aa', 'bb', function(aa, bb){})
等价于
var ep = new EventProxy()
ep.all('aa', 'bb', function(aa, bb){})
```

## 重复异步协作

例如，在读取多个文件结束后，再统一进行处理。

使用ep.after

```
var ep = new EventProxy()
ep.after('got_file', files.length, function(list) {
//所有文件的内容都存放在list数组里。
})
for(let i=0; i<files.length; i++) {
	fs.readFile(files[i], function(err, content) {
		ep.emit('got_file', content)
	})
}
```

## 持续型异步协作

这里以股票为例。

数据和模板都是异步读取，但是数据会持续刷新。

视图也需要刷新。

```
var ep = new EventProxy()
ep.tail('tpl', 'data', function(tpl, data) {
//
})
fs.readFile('template.tpl', function(err, content) {
	ep.emit('tpl', content)
})
setInterval(function() {
	db.get('some sql', function(err, result) {
		ep.emit('data', result)
	})
}, 2000)
```

ep.tail和ep.all，看起来类似，都是注册事件组合。

不同在于：tail在在指定事件都触发后，如果事件持续触发，则每次触发都调用最后的处理。

代码实现上的区别就是一个点：all在这里是push true。表示是否只执行一次。

![image-20210103150502368](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210103150502368.png)

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



# 和async库的对比

这里说的async库，不是js的async关键字。

https://github.com/caolan/async

```
var fs = require('fs')
var eventproxy = require('eventproxy')
var ep = new eventproxy()

ep.all(['read1', 'read2'], function(txt1, txt2) {
    console.log('txt1:' + txt1)
    console.log('txt2:' + txt2)
})

fs.readFile('1.txt', ep.done('read1'))
fs.readFile('2.txt', ep.done('read2'))
```

ep.done还可以这样写。

```
fs.readFile('1.txt', ep.done(function(data) {
    ep.emit('read1', data)
}))
```

使用after

```
ep.after('read', 2, function(data) {
    console.log(data)
})
ep.emit('read', '123')
ep.emit('read', 'abc')
```

打印是这样：

```
[ '123', 'abc' ]
```



什么时候使用eventproxy，什么时候用async库？

当需要去多个数据源获取数据，然后进行组合汇总的，这样的场景，用eventproxy更加方便。

当需要用到队列，需要控制并发数的，或者需要方便使用函数式编程的时候，使用async。



# 例子

读2个文件，把内容组合起来。相当于多个异步结果的组合。

出错了。则是undefined。

```
var fs = require('fs')
var eventproxy = require('eventproxy')

var ep = new eventproxy()
ep.all('file1', 'file2', function(data1, data2) {
    console.log(`data1:${data1}`)
    console.log(`data2:${data2}`)
})
fs.readFile('1.txt', function(err, data) {
    ep.emit('file1', data)

})
fs.readFile('2.txt', function(err, data) {
    ep.emit('file2', data)
})

```



```
var ep = new eventproxy()
ep.all('file1', 'file2', function(data1, data2) {
    console.log(`data1:${data1}`)
    console.log(`data2:${data2}`)
})
等价于
var ep = eventproxy.create('file1','file2', function(data1, data2) {
    
})
```

同一个操作做多次

```
var fs = require('fs')
var eventproxy = require('eventproxy')

var ep = new eventproxy()
files = ['1.txt', '2.txt']

ep.after('get_data', files.length, function(list) {
    for(let i=0; i<list.length; i++) {
        console.log(`data[${i}]:${list[i]}`)
    }
})
for(let i=0;i<files.length; i++) {
    fs.readFile(files[i], function(err, data) {
        ep.emit('get_data', data)
    })
}
```

持续异步协作

```
var fs = require('fs')
var eventproxy = require('eventproxy')

var ep = new eventproxy()
ep.tail('file1', 'file2', function(data1, data2) {
    console.log(`data1:${data1}`)
    console.log(`data2:${data2}`)
})
fs.readFile('1.txt', function(err, data) {
    ep.emit('file1', data)
})
setInterval(function() {
    fs.readFile('2.txt', function(err, data) {
        ep.emit('file2', data)
    })
}, 2000)

```

这个的运行效果是，每两秒，都把data1和data2一起打印出来。

```
data1:123
data2:abc
data1:123
data2:abc
data1:123
data2:abc
```

# 异常处理

```
var fs = require('fs')
var eventproxy = require('eventproxy')

var getContent = function(callback) {
    var ep = new eventproxy()
    ep.all('file1', 'file2', function(data1, data2) {
        callback(null, {data1,data2})
    })
    ep.fail(callback)
    fs.readFile('1.txt', function(err, data) {
        if(err) {
            ep.emit('error', err)
            return
        }
        ep.emit('file1', data)
    })

    fs.readFile('3.txt', function(err, data) {
        if(err) {
            ep.emit('error', err)
            return
        }
        ep.emit('file2', data)
    })
}
function contentProcess(err, data) {
    if(err) {
        console.log('err happens')
        return
    }
    console.log(data)
}
getContent(contentProcess)
```



```
ep.emit('error', err)
等价于
ep.throw(err)
```



# 参考资料

1、使用 eventproxy 控制并发

http://wiki.jikexueyuan.com/project/node-lessons/eventproxy.html

2、async和eventproxy在流程控制上哪个更优秀

https://yijiebuyi.com/blog/1dcc27614c599b0f37a8aa5e1292a3ad.html