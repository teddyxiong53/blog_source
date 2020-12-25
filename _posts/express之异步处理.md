---
title: express之异步处理
date: 2020-12-24 17:51:30
tags:
- express
---



# 回调方式

```
var express = require('express')

var app = express()
function asyncFn(req, res, next) {
    setTimeout(()=> {
        console.log("asyncFn")
        next()
    }, 2000)
}

function asyncFn2(req, res, next) {
    setTimeout(()=> {
        console.log("asyncFn2")
        next()
    }, 2000)
}
function asyncFn3(req, res, next) {
    setTimeout(()=> {
        console.log("asyncFn3")
        res.send("end of process")
    }, 2000)
}

app.get('/', asyncFn, asyncFn2, asyncFn3)

app.listen(8080)
```

会等6秒，才得到回复。

每一步需要2秒。跟预期一致。



参考资料

1、Express异步进化史

https://www.cnblogs.com/humin/p/7497996.html

