---
title: express之body-parser
date: 2019-05-09 16:24:11
tags:
	- nodejs

---

1

body-parser是express非常常用的一个中间件。

主要作用是对post的请求body进行解析。

```
const bodyParser = require('body-parser');
//对body-parser进行配置
app.use( bodyParser.urlencoded({extended: true}) )
//设置完毕之后，会在req对象上面新增一个req.body的一个对象
```

4.7.2版本的express没有了bodyParser方法,需要另外安装body-parser模块

```
var express = require('express');
var bodyParser = require('body-parser');
var app = express();

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }));

// parse application/json
app.use(bodyParser.json());
```



body-parser不能处理multipart的body。因为这个复杂。

multipart的body，专门有中间件来处理，multer就是。

bodyParser会在req对象里，增加一个body成员。

如果没有body内容，那么body是一个空的对象。

content-type不匹配，有错误的时候，body也是空的对象。

bodyParser.json(options)

options的内容：

```
inflate
	默认是true。默认解压。
limit
	body的大小。默认100kb。
reviver
strict
	都是传递给json解析器的参数。
type
	默认是application/json
verify
	函数，格式：verify(req,res, buf, encoding)
```



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

2、body-parse的简单使用

https://blog.csdn.net/web_youth/article/details/80053187