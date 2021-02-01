---
title: express之使用async
date: 2021-01-27 10:11:11
tags:
	- express

---

--

express之所以是同步的，是因为中间件里，如果不调用next，那么就一直阻塞在当前这个中间件这里。

所以都是在当前中间件处理完成的回调函数里，调用的next。这样才继续往后传递的。

下面引入了async，并没有改变这个基本的原则。



我们在express的处理函数里，有不少的异步代码，例如读取数据库这些操作。

所以，就可以使用async和await来优化代码流程。

是这样来用

```
app.get('/test', async (req, res)=> {
	var user = await User.findOne({email:req.body.email})
	//...
})
```

我就用express写一个最小的例子来进行测试。

```
var express = require('express')

var app =express()

app.get('/', function(req,res, next) {
    res.send('hello express')
})

app.listen(9090, '0.0.0.0')
```

改成这样

```
async function test1() {
    return '123'
}
app.get('/', async function(req,res, next) {
    var data1 = await test1()

    res.send('hello express ' + data1)
})
```

可以正常返回。

然后故意加一个错误

```
app.get('/', async function(req,res, next) {
    var aa = req.body.aa//这个是错误的。
    var data1 = await test1()
    res.send('hello express ' + data1)
})
```

访问一下，服务端有报错。

```
(node:8412) UnhandledPromiseRejectionWarning: TypeError: Cannot read property 'aa' of undefined
    at /home/teddy/work/test/nodeclub-master/xhl.js:9:23
```

加上try catch看看。

```
app.get('/', async function(req,res, next) {
    try {
        var aa = req.body.aa
        var data1 = await test1()
        res.send('hello express ' + data1)
    } catch(error) {
        console.log('error happens here')
    }
})
```

我们可以把错误用next往后传递。

```
app.get('/', async function(req,res, next) {
    try {
        var aa = req.body.aa
        var data1 = await test1()
        res.send('hello express ' + data1)
    } catch(error) {
        console.log('error happens here')
        next('出错了')
    }
})
app.use(function(error, req, res, next) {
    return res.status(500).send(error)
})
```

这样网页上看到的是就是”出错了“这3个汉字。

然后我们再加一个异步函数test2，返回abc 3个字符。

```
async function test2() {
    return 'abc'
}
app.get('/', async function(req,res, next) {
    try {
        var data1 = await test1()
        var data2 = await test2()
        res.send('hello express ' + data1 + data2)
    } catch(error) {
        console.log('error happens here')
        next('出错了')
    }
})
```





参考资料

1、Using Async/await in Express

https://zellwk.com/blog/async-await-express/