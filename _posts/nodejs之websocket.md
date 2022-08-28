---
title: nodejs之websocket
date: 2020-08-28 08:43:08
tags:
	- nodejs

---

--

websocket协议本质上是一个基于tcp的协议。

为了建立一个websocket连接，浏览器需要：

1、向服务器发出一个http请求。这个请求带特殊的header。其中包含了`Upgrade: WebSocket`表示这个http请求的目的是进行协议升级。

2、服务器收到这个升级协议的请求后，同意并进行应答。

3、然后浏览器和服务器的websocket连接建立成功。双方可以互相发消息。

4、这个连接持续到任意一方主动断开连接为止。

# HelloWorld

websocket api是纯事件驱动的。

我们看看设备端的写法：

新建一个html。

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        function websocketTest() {
            if ('WebSocket' in window) {
                alert('你的浏览器支持websocket')
                var ws = new WebSocket('ws://10.28.8.24:9999')
                ws.onopen = function() {
                    ws.send('客户端发送websocket消息')
                }
                ws.onmessage = function(evt) {
                    var msg = evt.data;
                    console.log(msg)
                    alert(`收到服务端的消息:${msg}`)
                }
                ws.onclose =  function() {
                    alert('websocket连接已经关闭')
                }
            }
        }
    </script>
    <div>
        <a href="javascript:websocketTest()">运行websocket</a>
    </div>
</body>
</html>
```



服务端的写法

nodejs里websocket有：

1、uwebsocket。

2、socket.io。

3、websocket-node。

4、ws库。

我们就是用ws库来作为例子。

```
npm i -s ws
```

新建server.js，内容如下：

```
var WebSocketServer = require('ws').Server
server = new WebSocketServer({
    port: 9999
})

server.on('connection', function(conn) {
    conn.on('message', function(msg) {
        console.log(`recv msg: ${msg}`)
        conn.send("我是websocket服务器")
    })
})
```

然后就可以进行测试 了。

# 模拟股票数据刷新



# 参考资料

1、

https://blog.csdn.net/zhouzuoluo/article/details/89312798