---
title: nodejs之实现静态文件服务器
date: 2019-08-31 15:22:03
tags:
	- nodejs
---

1

新建目录如下：

```
hlxiong@hlxiong-VirtualBox:~/work/test/nodejs/nodejs-static-webserver$ tree
.
├── app.js
├── config
│   └── default.json
├── package.json
└── static-server.js
```

static-server.js

```
var http = require("http")
var path = require("path")
var config = require("./config/default")

class StaticServer {
    constructor() {
        this.port = config.port
        this.root = config.root
        this.indexPage = config.indexPage
    }
    start() {
        http.createServer((req, res) =>{
            var pathName = path.join(this.root, path.normalize(req.url))
            res.writeHead(200)
            res.end(`request path:${pathName}`)

        }).listen(this.port, err=> {
            if(err) {
                console.log("listen fail:", err)
            } else {
                console.log("listen on " + this.port)
            }
        })
    }

}
module.exports = StaticServer
```

app.js

```
var StaticServer = require("./static-server")

var server = new StaticServer()
server.start()
```

default.json

```
{
    "port": 3000,
    "root": "/home/hlxiong/work/test/nodejs/nodejs-static-webserver",
    "indexPage": "index.html"
}
```

现在可以运行，访问一下。

现在只是打印了文件路径而已，接下来，我们需要把文件发送到客户端。



参考资料

1、使用Node.js搭建静态资源服务器

https://www.cnblogs.com/SheilaSun/p/7271883.html