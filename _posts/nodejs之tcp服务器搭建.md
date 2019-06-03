---
title: nodejs之tcp服务器搭建
date: 2019-05-31 17:39:51
tags:
	- nodejs

---



代码很简单：

```
var net = require("net")

var server = net.createServer(function(socket) {
    console.log(socket.address());
})

server.listen(4000, function() {
    console.log("listen on 4000");
})
```

运行效果：

```
hlxiong@hlxiong-VirtualBox:~/work/test/libhttpclient/webserver$ node tcp_server.js 
listen on 4000
{ address: '::ffff:192.168.56.101', family: 'IPv6', port: 4000 }
```



```
var net = require("net")

var server = net.createServer(function(socket) {
    console.log(socket.address());
    socket.on('data', function(data) {

        if(data.toString() == "hello") {//收到hello，回复hello。
            console.log(data.toString())
            var readSize = socket.bytesRead;
            console.log("data size: ", readSize);
            socket.write(data.toString(), function() {
                console.log("write back to client:", socket.bytesWritten);
            })
        } else {//其他数据，发送2000字节的0x01 。
            console.log(data);//这个打印就是十六进制的内容。
            const buf = Buffer.alloc(2000, 1);
            socket.write(buf, function() {
                console.log("write to client:", socket.bytesWritten);
            })
        }

    })
})

server.listen(4000, function() {
    console.log("listen on 4000");
})

```



参考资料

1、

https://zc95.github.io/2018/03/20/nodejs-TCP/