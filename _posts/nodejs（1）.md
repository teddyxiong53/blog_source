---
title: nodejs（1）
date: 2018-11-03 14:27:19
tags:
	- nodejs

---



从man node的信息来看，nodejs是Server side JavaScript Runtime。

是基于谷歌的一个c++的JavaScript引擎来写。

我看百度有不少的demo都有node.js的版本。

所以这个也算是一个快速搭建应用的一种方式。感觉挺有用的。所以花点时间学习一下。

还是以菜鸟教程上的资料为主要学习材料。

我都用Ubuntu默认安装的版本，其实确认是很老的了。但是我先不管，后面有问题了再升级。

```
teddy@teddy-ubuntu:~/work/nodejs$ npm -v
3.5.2
teddy@teddy-ubuntu:~/work/nodejs$ nodejs -v
v4.2.6
```

# 最简单的程序

```
console.log("hello node.js");
```

然后运行：

```
nodejs test.js
```

这个的效果，就是打印“hello node.js”。

# 启动一个web server

也是几行代码就够了。

```
var http = require("http");
http.createServer(
    function (request, response) {
        response.writeHead(200, {'Content-Type': 'text/plain'});
        response.end('hello world\n');
    }

).listen(8080);
console.log("service running at 0.0.0.0:8080");
```

然后访问这地址，可以看到hello world的打印。

# repl

跟Python类似，但是感觉没有Python强大。

```
teddy@teddy-ubuntu:~/work/nodejs$ nodejs
> 1+1
2
> 20*40+330
1130
```

# 回调函数

node.js异步编程的直接体现就是回调。

node是所有api函数都支持回调。

通过回调，实现了程序的并行，不会阻塞在IO上，提高了效率。

回调函数一般作为函数的最后一个参数。

举例：

```
function foo1(name, age, callback) {
	
}

function foo2(value, callback1, callback2) {
	
}
```

阻塞代码，读取文件。

```
var fs = require("fs");
var data = fs.readFileSync("input.txt");
console.log(data.toString());
console.log("end of code");
```

效果：

```
teddy@teddy-ubuntu:~/work/nodejs$ nodejs test.js 
abc
123
xxx

end of code
```



非阻塞版本。

```
var fs = require("fs");
fs.readFile("input.txt", function (err, data) {
	if(err) {
		return console.error(err);
	}
	console.log(data.toString());
});
console.log("end of code");
```

效果：

```
teddy@teddy-ubuntu:~/work/nodejs$ nodejs test.js 
end of code
abc
123
xxx
```

# 事件循环

node是单进程单线程的应用。但是因为V8引擎提供的回调机制，所以并发效率还是很高的。

事件机制是用设计模式里的观察者模式。

node有多个内置的事件，我们可以通过引入events事件，并通过实例化EventEmitter来绑定和监听event。

```
var events = require('events');
var eventEmitter = new events.EventEmitter();

var connectHandler = function connected() {
	console.log("connect ok");
	eventEmitter.emit("data_received");
}

eventEmitter.on("connection", connectHandler);
eventEmitter.on("data_received", function() {
	console.log("receive data ok");
});

eventEmitter.emit("connection");
console.log("end of code");
```

# Buffer

js语言本身没有二进制数据类型，只有字符串数据类型。

在处理tcp流或者文件流的时候，必须使用二进制数据。

所以node.js，定义了一个Buffer类。专门用来存放二进制数据。

Buffer本质上类似一个整数数组。对应V8引擎之外的一块内存。

##创建Buffer

现在官方建议用Buffer.from方法创建Buffer对象，之前都是new Buffer的方式。

```
const buf = Buffer.from("aaa", "ascii");
console.log(buf.toString('hex'));
console.log(buf.toString('base64'));
```

from函数的第二个参数是编码类型。

可以是：

1、ascii。

2、utf8

3、utf16e

4、ucs2。这个是utf16e的别名。

5、base64 。

6、latin1.

7、binary。latin1的别名。

8、hex。

Buffer创建的其他方法：

```
//创建一个长度为10，并且用0填充的buffer
const buf1 = Buffer.alloc(10);
//创建一个长度为10，并且用1填充的buffer。
const buf2 = Buffer.alloc(10, 1);
//创建一个长度为，没有初始化的buffer，里面是随机值
//这个优点是速度快一点。我感觉没有实际好处。
const buf3 = Buffer.allocUnsafe(10);
//创建一个包含[1,2,3]buffer
const buf4 = Buffer.from([1,2,3]);
```

## 写入Buffer

```

```

## 从Buffer读取







# 参考资料

1、node.js教程

http://www.runoob.com/nodej



