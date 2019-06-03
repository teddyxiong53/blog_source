---
title: nodejs之protobuf
date: 2018-12-28 17:57:17
tags:
	- nodejs

---



在安装的node_modules目录下，有个readme，里面有详细说明。

网上很多的文章，都不对了。太老了。

写一个awesome.proto。

```
package awesomepackage;
syntax = "proto3";
message AwesomeMessage {
    string awesome_field = 1;
}
```

```
const protobuf = require("protobufjs");
protobuf.load("awesome.proto", function(err, root) {
    if(err) {
        throw err;
    }
    var AwesomeMessage = root.lookupType("awesomepackage.AwesomeMessage");
    var payload = {awesomeField: "AwesomeString"};
    var errMsg = AwesomeMessage.verify(payload);
    if(errMsg) {
        throw Error(errMsg);
    }
    var message = AwesomeMessage.create(payload);
    var buffer = AwesomeMessage.encode(message).finish();
    //do something with buffer
    //...
    console.log(buffer);
    var message = AwesomeMessage.decode(buffer);

    var object = AwesomeMessage.toObject(message, {
        longs: String,
        enums: String,
        bytes: String,
    });
    console.log(object);
});
```

运行效果：

```
hlxiong@hlxiong-VirtualBox:~/work/test/protobuf$ node test.js 
<Buffer 0a 0d 41 77 65 73 6f 6d 65 53 74 72 69 6e 67>
{ awesomeField: 'AwesomeString' }
```



# 更实用的例子

一个client和一个server，用udp协议。

注意这个代码对protobufjs的版本有要求：

```
npm install protobufjs@5.0.1 --save
```



cover.helloworld.proto文件

```
package cover;

message helloworld {

    message helloCoverReq {
        required string name = 1;
    }

    message helloCoverRsp {
        required int32 retcode = 1;
        optional string reply = 2;
    }
}
```

sever.js

```
var PORT = 33333;
var HOST = '127.0.0.1';
var ProtoBuf = require("protobufjs");
var dgram = require('dgram');
var server = dgram.createSocket('udp4');

var builder = ProtoBuf.loadProtoFile("./cover.helloworld.proto"),
    Cover = builder.build("cover"),
    HelloCoverReq = Cover.helloworld.helloCoverReq;
    HelloCoverRsp = Cover.helloworld.helloCoverRsp;

server.on('listening', function () {
    var address = server.address();
    console.log('UDP Server listening on ' + address.address + ":" + address.port);
});

server.on('message', function (message, remote) {
    console.log(remote.address + ':' + remote.port +' - ' + message);
    console.log(HelloCoverReq.decode(message) + 'from client!');
    var hCRsp = new HelloCoverRsp({
        retcode: 0,
        reply: 'Yeah!I\'m handsome cover!'
    })

    var buffer = hCRsp.encode();
    var message = buffer.toBuffer();
    server.send(message, 0, message.length, remote.port, remote.address, function(err, bytes) {
        if(err) {
            throw err;
        }

        console.log('UDP message reply to ' + remote.address +':'+ remote.port);
    })

});

server.bind(PORT, HOST);
```

client.js

```
var dgram = require('dgram');
var ProtoBuf = require("protobufjs");
var PORT = 33333;
var HOST = '127.0.0.1';

var builder = ProtoBuf.loadProtoFile("./cover.helloworld.proto"),
    Cover = builder.build("cover"),
    HelloCoverReq = Cover.helloworld.helloCoverReq;
    HelloCoverRsp = Cover.helloworld.helloCoverRsp;

var hCReq = new HelloCoverReq({
    name: 'R U coverguo?'
})


var buffer = hCReq.encode();

var socket = dgram.createSocket({
    type: 'udp4',
    fd: 8080
}, function(err, message) {
    if(err) {
        console.log(err);
    }

    console.log(message);
});

var message = buffer.toBuffer();

socket.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
    if(err) {
        throw err;
    }

    console.log('UDP message sent to ' + HOST +':'+ PORT);
});

socket.on("message", function (msg, rinfo) {
    console.log("[UDP-CLIENT] Received message: " + HelloCoverRsp.decode(msg).reply + " from " + rinfo.address + ":" + rinfo.port);
    console.log(HelloCoverRsp.decode(msg));

    socket.close();

    //udpSocket = null;
});

socket.on('close', function(){
    console.log('socket closed.');


});

socket.on('error', function(err){
    socket.close();

    console.log('socket err');
    console.log(err);
});
```



参考资料

1、

https://www.cnblogs.com/wuyuchao/p/9229877.html

2、

https://imweb.io/topic/570130a306f2400432c1396c



