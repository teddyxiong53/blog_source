---
title: nodejs之socket编程
date: 2018-12-23 16:57:11
tags:
	- nodejs

---



新建server.js。

```
var net = require('net')
var port = 8080
var server = net.createServer(function(socket) {
    console.log("connect: " + socket.remoteAddress + ": " + socket.remotePort)
    socket.setEncoding('binary')
    socket.on('data', function(data) {
        console.log("client send: " + data);
    })
    socket.write("hello client\n")
    socket.on('error', function(exception) {
        console.log("socket error: " + exception)
        socket.end()
    })
    socket.on('close', function(data) {
        console.log('client close')
    })

}).listen(port)

server.on('listening', function() {
    console.log('server listening' + server.address().port)
})

```

新建client.js

```
var net = require("net")
var port = 8080
var host = "127.0.0.1"
var client = new net.Socket()

client.setEncoding('binary')
client.connect(port, host, function() {
    client.write('hello server')
})
client.on('data', function(data) {
    console.log('from server: ' + data)
})

client.on('close', function() {
    console.log('connection closed')
})

```



# 参考资料

1、nodejs socket实现的服务端和客户端简单通信

https://blog.csdn.net/lockey23/article/details/76408891