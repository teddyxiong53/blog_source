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



参考资料

1、

https://www.cnblogs.com/wuyuchao/p/9229877.html





