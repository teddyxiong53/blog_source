---
title: nodejs之async模块
date: 2020-12-30 13:25:11
tags:
	- nodejs

---

1

看cnode的代码，里面有用到async这个模块。

在早期的异步开发中， Async 模块是比较有名的异步解决方案。

有些代码，需要依赖多个回调的执行结果。可能需要依赖的东西以某种特定的顺序执行。或者平时执行。

为了方便这种流程控制，可以借助async模块。

async模块是在js引入Promise等机制之前就有的。

async模块方法有很多。我们重点看3个：

```
async.parallel()//并联
async.series()//串联，后面的函数不依赖前面函数的输出。
async.waterfall()//后一步使用前面一步的结果。
```

上面3个函数里，可以传递一个对象，也可以传递数组。

但是，因为js里，对象的枚举顺序是不确定的，如果对函数的执行顺序有要求。

就要使用数组的方式来传递。



async 的思路是将原本容易出现 callback hell 的嵌套，

通过数组并列的方式抹平，

并且节省每次判断 error 的代码，

按照 error first 的约定在内部每次都帮助用户检查异步是否出错。

了解了这种想法之后我们可以写个很简单的 waterfall 出来。



```
const async = require('async')
async.series([
    function step1(cb) {
        console.log("step1")
        cb(null, "step1")
    },
    function step2(cb) {
        console.log("step2")
        cb(null, "step2")
    }
], function(err, result) {
    console.log("end")
})
```

注意：函数都要有一个cb参数，并且进行调用，这样才能往后面传递。

cb的的第一个参数是错误，如果不是null，则直接跳过中间的，到最后的错误处理函数里。

要演示延时的情况。可以这样：

```
const async = require('async')
async.series([
    function step1(cb) {
        console.log("step1")
        setTimeout(function() {
            cb(null, "step1")
        }, 1000)

    },
    function step2(cb) {
        console.log("step2")
        setTimeout(function() {
            cb(null, "step2")
        }, 1000)
    }
], function(err, result) {
    console.log("end")
})
```

看看waterfall的

它因为需要把返回值往后传递，所以跟series和parallel不同。

```
const async = require('async')
async.waterfall([
    function step1(cb) {
        console.log("step1")
        setTimeout(function() {
            cb(null, "第一步返回值")
        }, 1000)

    },
    function step2(res, cb) {
        console.log("step2")
        console.log("第一步传递过来的值："+res)
        setTimeout(function() {
            cb(null, "step2")
        }, 1000)
    }
], function(err, result) {
    console.log("end")
})
```



参考资料

1、使用 async 进行非同步流控制

https://developer.mozilla.org/zh-CN/docs/learn/Server-side/Express_Nodejs/Displaying_data/flow_control_using_async

2、Async 模块实现入门浅析

https://zhuanlan.zhihu.com/p/27303127