---
title: nodejs之express
date: 2018-12-18 20:28:55
tags:
	- nodejs

---



express 是一个web应用框架。用来快速搭建一个网站的。

核心功能：

1、可以设置中间件来响应http请求。

2、定义路由表来执行不同的http请求动作。

3、可以通过向模板传递参数来动态渲染html页面。



# 安装及使用

```
npm install -g express
```

我当前安装的是4.16.4的。

```
hlxiong@hlxiong-VirtualBox:~/work/test/express$ npm install express -g
+ express@4.16.4
added 48 packages from 36 contributors in 6.686s
```

写一个helloworld。

新建express_demo.js。

```
const express = require("express");
var app = express();
app.get("/", function(req, res) {
    res.send("hello express");
});

var server = app.listen(8080, "0.0.0.0", function() {
    console.log("server listen on 8080");
});
```

node express_demojs。就可以访问了。

重点是request对象和Response对象。

我可以通过node的repl来探索他们的属性。

用tab提示看看有哪些属性。

但是nodejs的repl没有像python那样的help函数可以查看这些接口的详细信息。

所以我还是在vscode里来查看。

加打印看看。

```
app.get("/", function(req, res) {
    console.log("req.app type:", typeof req.app);
    console.log("req.baseUrl:", req.baseUrl);
    console.log("req.body:", req.body);
    console.log("req.hostname:", req.hostname);
    console.log("req.ip:", req.ip);
    console.log("req.orignalUrl:", req.originalUrl);
    console.log("req.params:", req.params);
    console.log("req.path:", req.path);
    console.log("req.protocol:", req.protocol);
    console.log("req.query:", req.query);
    console.log("req.route:", req.route);
    console.log("req.subdomains", req.subdomains);
    console.log("req.accepts:", req.accepts);
    console.log("req.acceptsCharsets:", req.acceptsCharsets);
    console.log("req.get:", req.get("Content-Type"));
    res.send("hello express");
});
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/express$ node express_demo.js 
server listen on 8080
req.app type: function
req.baseUrl: 
req.body: undefined
req.hostname: 192.168.56.101
req.ip: 192.168.56.1
req.orignalUrl: /
req.params: {}
req.path: /
req.protocol: http
req.query: {}
req.route: Route {
  path: '/',
  stack:
   [ Layer {
       handle: [Function],
       name: '<anonymous>',
       params: undefined,
       path: undefined,
       keys: [],
       regexp: /^\/?$/i,
       method: 'get' } ],
  methods: { get: true } }
req.subdomains []
req.accepts: function(){
  var accept = accepts(this);
  return accept.types.apply(accept, arguments);
}
req.acceptsCharsets: function(){
  var accept = accepts(this);
  return accept.charsets.apply(accept, arguments);
}
req.get: undefined
```



# 路由

前面我们已经了解了基本的请求。

路由就是分配谁去响应某个请求。

```
const express = require("express");
var app = express();
app.get("/", function(req, res) {
    console.log("主页get请求");
    res.send("hello get");
});

app.post("/", function(req, res) {
    console.log("主页post请求");
    res.send("hello post");
});

app.get("/del_user", function(req, res) {
    console.log("/del_user响应delete请求");
    res.send("hello del_user");
});

app.get("/list_user", function(req, res) {
    console.log("/list_user 响应");
    res.send("hello list_user");
});

app.get("/ab*cd", function(req, res) {
    console.log("/ab*cd响应");
    res.send("正则匹配");
});

var server = app.listen(8080, "0.0.0.0", function() {
    console.log("server listen on 8080");
});
```



# 静态文件

当前目录新建一个public目录，下面新建一个images目录，下面放一个logo.png文件。

express_demo.js如下：

```
加上这句：
app.use(express.static("public"));
相当于是把public设置为静态目录的顶层目录，在url里使用的时候，从public的子目录写起就可以了。
```

访问：http://192.168.56.101:8080/images/logo.png



现在目录如下：

```
.
├── index.html
├── public
│   └── images
│       └── logo.png
└── server.js
```

index.html：

```
<html>
    <body>
        <form action="/process_get" method="GET">
            first name: <input type="text" name="first_name"><br>
            last name: <input type="text" name="last_name"><br>
            <input type="submit" value="提交">
        </form>
    </body>
</html>
```

server.js：

```
const express = require("express");
var app = express();
app.use(express.static("public"));

app.get("/index.html", function(req, res) {
    res.sendFile(__dirname + "/"  + "index.html");
});
app.get("/process_get", function(req, res) {
    var response = {
        "first_name": req.query.first_name,
        "last_name": req.query.last_name
    };
    res.end(JSON.stringify(response));
})
var server = app.listen(8080, "0.0.0.0", function() {
    console.log("server listen on 8080");
});
```

访问http://192.168.56.101:8080/index.html

填好，提交。得到返回的连接是这个。

http://192.168.56.101:8080/process_get?first_name=a&last_name=b

网页内容是：

```
{first_name":"a","last_name":"b"}
```

测试post方法。

server.js

```
const express = require("express");
var app = express();
var bodyParser = require("body-parser");

var urlencodedParser = bodyParser.urlencoded({extended: false});

app.use(express.static("public"));

app.get("/index.html", function(req, res) {
    res.sendFile(__dirname + "/"  + "index.html");
});
//方法改成了post。
app.post("/process_post", urlencodedParser,  function(req, res) {
    var response = {
        "first_name": req.body.first_name,//这里改成了body，get的是query。
        "last_name": req.body.last_name
    };
    res.end(JSON.stringify(response));
})
var server = app.listen(8080, "0.0.0.0", function() {
    console.log("server listen on 8080");
});
```

index.html

```
<html>
    <body>
        <form action="/process_post" method="POST">
            first name: <input type="text" name="first_name"><br>
            last name: <input type="text" name="last_name"><br>
            <input type="submit" value="提交">
        </form>
    </body>
</html>
```

# 上传文件

先修改index.html如下：

```
<html>
    <body>
        <h3>选择一个文件上传</h3>
        <form action="/file_upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="image" size="50"><br>
            <input type="submit" value="上传文件">
        </form>
    </body>
</html>
```

server.js：

```
const express = require("express");
var app = express();
var fs = require("fs");

var bodyParser = require("body-parser");
var multer = require("multer");

app.use(express.static("public"));
app.use(bodyParser.urlencoded({extended: false}));
app.use(multer({dest: "/tmp"}).array("image"));

app.get("/index.html", function(req, res) {
    res.sendFile(__dirname + "/"  + "index.html");
});

app.post("/file_upload", function(req, res) {
    console.log(req.files[0]);
    var dest_file = __dirname + "/" + req.files[0].originalname;
    fs.readFile(req.files[0].path, function(err, data) {
        fs.writeFile(dest_file, data, function(err) {
            if(err) {
                console.log(err);
            } else {
                response = {
                    message: "File upload ok",
                    filename: req.files[0].originalname
                };
            }
            console.log(response);
            res.end(JSON.stringify(response));
        });
    });
});

var server = app.listen(8080, "0.0.0.0", function() {
    console.log("server listen on 8080");
});
```

输出：

```
hlxiong@hlxiong-VirtualBox:~/work/test/express$ node server.js 
server listen on 8080
{ fieldname: 'image',
  originalname: '1.png',
  encoding: '7bit',
  mimetype: 'image/png',
  destination: '/tmp',
  filename: '7537a82c0aa2700ed20d23ddacc7ae1f',
  path: '/tmp/7537a82c0aa2700ed20d23ddacc7ae1f',
  size: 2292 }
{ message: 'File upload ok', filename: '1.png' }
```



# app.get和app.use区别

看N-blog的代码，看到有的时候用app.get，有的用app.use。

有什么规律？

app.get相当于app.use的get方法版本。

一般在很简单的时候用。





# 官网资料学习

安装生成器。

```
npm install express-generator -g
```

这样会得到express命令。

执行效果是这样，得到这样的目录结构。可以直接运行。

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ tree
.
├── app.js
├── bin
│   └── www
├── package.json
├── public
│   ├── images
│   ├── javascripts
│   └── stylesheets
│       └── style.css
├── routes
│   ├── index.js
│   └── users.js
└── views
    ├── error.jade
    ├── index.jade
    └── layout.jade
```

运行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ npm start     

> node@0.0.0 start /home/hlxiong/work/test/node
> node ./bin/www

GET / 200 648.894 ms - 170
GET /stylesheets/style.css 200 16.330 ms - 111
GET /favicon.ico 404 32.348 ms - 1102
GET /favicon.ico 404 21.055 ms - 1102
```

访问127.0.0.1:3000就可以了。



# 参考资料

1、Node.js Express 框架

http://www.runoob.com/nodejs/nodejs-express-framework.html

2、

https://blog.csdn.net/wthfeng/article/details/53366169