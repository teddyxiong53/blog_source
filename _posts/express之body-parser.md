---
title: express之body-parser
date: 2019-05-09 16:24:11
tags:
	- nodejs

---

1

body-parser是express非常常用的一个中间件。

主要作用是对post的请求body进行解析。



# text/plain

client.js

```
var http = require("http")

var options = {
    host: '127.0.0.1',
    port: '3000',
    path: '/test',
    method: 'POST',
    headers : {
        'Content-Type': 'text/plain',
        'Content-Encoding': 'indentity'
    }
}

var client = http.request(options, (res)=> {
    res.pipe(process.stdout)
})

client.end("teddy")
```

server.js

```
var http = require("http")

var parsePostBody = function(req, done) {
    var arr = []
    var chunks = null
    req.on("data", buff=> {
        console.log("data:",buff)
        arr.push(buff)
    })
    req.on("end", ()=> {
        chunks = Buffer.concat(arr)
        done(chunks)
    })
}

var server = http.createServer(function(req, res) {
    parsePostBody(req, (chunks)=> {
        var body = chunks.toString()
        res.end(`your nick name is ${body}`)
    })
})

server.listen(3000)
```

# text/json

client.js

```
var http = require("http")

var options = {
    host: '127.0.0.1',
    port: '3000',
    path: '/test',
    method: 'POST',
    headers : {
        'Content-Type': 'text/json',
        'Content-Encoding': 'indentity'
    }
}

var client = http.request(options, (res)=> {
    res.pipe(process.stdout)
})
var data = {
    nick: 'teddy'
}
client.end(JSON.stringify(data))

```

server.js

```
var http = require("http")

var parsePostBody = function(req, done) {
    var arr = []
    var chunks = null
    req.on("data", buff=> {
        console.log("data:",buff)
        arr.push(buff)
    })
    req.on("end", ()=> {
        chunks = Buffer.concat(arr)
        done(chunks)
    })
}

var server = http.createServer(function(req, res) {
    parsePostBody(req, (chunks)=> {
        var data = JSON.parse(chunks.toString())
        res.end(`your nick name is ${data.nick}`)
    })
})

server.listen(3000)
```

# application/x-www-form-urlencoded

这个需要引入querystring。

就是把上面json的，替换成querystring就好了。



参考资料

1、Nodejs 进阶：Express 常用中间件 body-parser 实现解析

https://www.cnblogs.com/chyingp/p/nodejs-learning-express-body-parser.html

