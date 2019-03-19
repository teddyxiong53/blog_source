---
title: nodejs之socket.io
date: 2019-03-16 15:09:11
tags:
	- nodejs
---





在html5之前，因为http协议是无状态的。要实现浏览器跟服务器的实时通信，如果不使用flash、applet等浏览器插件的话，就需要定时轮询服务器来获取信息。

这种方式有一定的延时，而且导致了大量的网络通信。

随着html5的出现，这一情况有望彻底改观。

这个解决方案就是WebSocket。

理论上，tcp socket能干的一切，WebSocket都可以做。



WebSocket的工作机制

WebSocket的本质上就是一个tcp连接。

1、浏览器通过js代码，向服务器发送一个建立WebSocket连接的Request。

这个请求跟普通的http请求略有不同。头部多了一些信息。

其中有一个这样的字段：

```
Upgrade: WebSocket
```

表示这是一个申请协议升级的http请求。服务器解析这些信息后，产生应答信息给浏览器。

这样浏览器跟服务器之间的WebSocket连接就建立起来了。

双方可以通过这个通道自由地传递信息。

这个连接会持续到某一方关闭连接为止。



一个典型的协议是这样：

浏览器到服务器

```
GET / HTTP/1.1
Connection: Upgrade
host:127.0.0.1:8080
Origin: null
Sec-WebSocket-Extensions: x-webkit-deflate-frame
Sec-WebSocket-Key: XXXX
Sec-WebSocket-Version:13
Upgrade: websocket
```

服务器到浏览器

```
HTTP/1.1 101 Switching Protocols
Connection: Upgrade
Server: beetle websocket server
Upgrade: WebSocket
Date: xxx
Access-Control-Allow-Credentials:true
Access-Control-Allow-Headers: content-type
Sec-WebSocket-Accept:xxx
```



WebSocket可以跟http监听同一个端口，也可以使用自己单独的端口。



那么什么是socket.io呢？简单来说，socket.io是对WebSocket的封装。

实际上，socket.io还封装了轮询机制。

总共封装了这些机制：

```
1、AJAX long polling。这个就是定时向服务器轮询。
2、AJAX multipart streaming。
3、Forever iframe
4、JSONP Polling
```



# HelloWorld

这个HelloWorld由两部分组成。

client和server。

我们先写server端。

需要先安装nodejs的包。

```
npm install socket.io
```

新建目录如下：

```
hlxiong@hlxiong-VirtualBox ~/work/test/socket.io $ tree
.
├── client
│   └── index.html
└── server
    └── app.js
```

app.js内容：

```
var http = require("http")
var socket_io = require("socket.io")
var fs = require("fs")

var app = http.createServer(function(req, res) {
    fs.readFile(__dirname + "../client/index.html", function(err, data) {
        if(err) {
            res.writeHead(500);
            return res.end("error loading index.html")
        }
        res.writeHead(200);
        res.end(data);
    });


})
app.listen(3344)

var io = socket_io(app)

io.on("connection", function(socket) {
    socket.emit("news", {hello: "world"});
    socket.on("my other event", function(data) {
        console.log(data);
    });
});
```

index.html内容：

```
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js">

</script>

<script>
    var socket = io("http://localhost:3344");
    socket.on("news", function(data) {
        console.log(data);
        socket.emit("my other event", {my: "xx"})
    });
</script>
```

运行服务端：

```
hlxiong@hlxiong-VirtualBox ~/work/test/socket.io/server $ node app.js          
{ my: 'xx' } //这个在打开index.html才看到的。
```

然后用双击打开index.html文件。

就完成了测试。可以按F12看浏览器的控制台的打印。



# 聊天应用示例

使用传统的web应用技术栈，如lamp（php）来写一个聊天应用是困难的。

在传统技术栈上，只能通过轮询，还有追踪时间戳。这种实现效率是很低的。

大多数的实时聊天系统是基于socket的构建的。

新建一个chat-example目录。在这个目录下新建packag.json文件。

内容如下：

```
{
    "name": "socket-chat-example",
    "version": "1.0.0",
    "description": "my first socket.io app",
    "dependencies": {
        
    }
}
```

然后安装express。

```
npm install --save express
```

注意--save的效果，会修改package.json里。改成下面这样：

```
"dependencies": {
        "express": "^4.16.4"
}
```

然后新建一个index.js文件。内容如下：

```
var app = require("express")()
var http = require("http").Server(app)

app.get("/", function(req, res) {
    res.sendFile(__dirname + "/index.html");
});

http.listen(3344, function() {
    console.log("listen on 3344");
})
```

然后新建index.html。内容如下。

```
<!DOCTYPE html>
<html>
<head>
    <title>socket.io chat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font: 13px Helvetica, Arial;
        }
        form {
            background: #000;
            padding: 3px;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
        form input {
            border: 0;
            padding: 10px;
            width: 90%;
            margin-left: 0.5%;

        }
        form button {
            width: 9%;
            background: rgb(130,224,255);
            border: none;
            padding: 10px;
        }
        #messages {
            list-style-type: none;
            margin: none;
            padding: none;
        }
        #message li {
            padding: 5px 10px;
        }
        #message li:nth-child(odd) {
            background: #eee;
        }
    </style>
</head>
<body>
    <ul id="messages"></ul>
    <form action="">
        <input id="m" autocomplete="off"><button>Send</button>
    </form>
</body>
</html>
```

现在可以运行了。看看界面。

安装socket.io。

```
npm install --save socket.io
```

我们把index.js改成下面这样：

```
var app = require("express")()
var http = require("http").Server(app)
var io = require("socket.io")(http)

app.get("/", function(req, res) {
    res.sendFile(__dirname + "/index.html");
});

io.on("connection", function(socket) {
    console.log("a user connected");
    socket.on("disconnect", function() {
        console.log("user disconnected")
    });
    socket.on("chat message", function(msg) {
        console.log("message: " + msg);
    })
})

http.listen(3344, function() {
    console.log("listen on 3344");
})


```



socket.io的核心理念是允许发送、接收任意事件和任意数据。

任意能够被编码为json的对象都可以被传输。

二进制数据也是支持的。

把index.html改成这样：

```
<!DOCTYPE html>
<html>
<head>
    <title>socket.io chat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font: 13px Helvetica, Arial;
        }
        form {
            background: #000;
            padding: 3px;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
        form input {
            border: 0;
            padding: 10px;
            width: 90%;
            margin-left: 0.5%;

        }
        form button {
            width: 9%;
            background: rgb(130,224,255);
            border: none;
            padding: 10px;
        }
        #messages {
            list-style-type: none;
            margin: none;
            padding: none;
        }
        #message li {
            padding: 5px 10px;
        }
        #message li:nth-child(odd) {
            background: #eee;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js"></script>
    <script src="https://code.jquery.com/jquery-1.11.1.js"></script>
</head>
<body>
    <script>
        $(function() {
            var socket = io();
            $("form").submit(function() {
                socket.emit("chat message", $("#m").val());
                $("#m").val("");
                return false;
            })
        });
    </script>
    <ul id="messages"></ul>
    <form action="">
        <input id="m" autocomplete="off"><button>Send</button>
    </form>
</body>
</html>
```

现在访问http://192.168.56.101:3344，服务端的打印如下。

```
hlxiong@hlxiong-VirtualBox ~/work/test/socket.io/chat-example $ node index.js               
listen on 3344
a user connected
a user connected
message: aaa
```

现在服务端是拿到用户发来的信息了，接下来就是要把这个信息分发给所有的用户。

socket.io提供了一个emit方法。

我们在index.js里加一行代码就好了。

```
socket.on("chat message", function(msg) {
        console.log("message: " + msg);
        io.emit("chat message", msg);//加这行代码。
    })
```

接下来，我们需要在客户端搏或chat message事件，并把消息添加到页面上。

```
$(function() {
            var socket = io();
            $("form").submit(function() {
                socket.emit("chat message", $("#m").val());
                $("#m").val("");
                return false;
            });
            //加下面两行代码。
            socket.on("chat message", function(msg) {
                $("#messages").append($("<li>").text(msg));
            });
        });
```

到这里，就基本写完了一个聊天应用了。

当前还有很多可以优化的点：

```
1、在用户连接和断开时广播消息。
2、添加昵称。
3、添加用户正在输入功能。
4、显示在线用户。
5、添加私密消息。
```



# 服务端api



# 疑问

## socket.io.js在哪里？

我是用cdn的方式，但是我看其他人写的代码。

并没有指向cdn。

而是这样的：

```
<script src="/socket.io/socket.io.js"></script>
```

这个路径上有这个文件吗？

这个帖子提到了相同的疑问。

https://stackoverflow.com/questions/32571489/where-is-the-socket-io-js-file-located-at

解释是：

会到你的node_modules下面去找。



参考资料

1、SOCKET.IO，理解SOCKET.IO

https://www.cnblogs.com/xiezhengcai/p/3957314.html

2、socket.io官方文档

https://www.w3cschool.cn/socket/socket-1olq2egc.html

3、socket.io的前端的cns列表。

https://cdnjs.com/libraries/socket.io