---
title: nodejs（1）
date: 2018-11-03 14:27:19
tags:
	- nodejs

---

--

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

# nodejs简介

Node.js是一种基于Chrome V8引擎的JavaScript运行环境，可以让你用JavaScript语言开发后端服务器端应用程序。它采用事件驱动、非阻塞式I/O模型，使得它非常适合处理高并发的网络应用。Node.js的特点包括：

1. **基于事件驱动的异步I/O**: Node.js使用事件驱动的方式处理I/O操作，这使得它在处理大量并发连接时非常高效。

2. **单线程、非阻塞**: Node.js采用单线程模型来处理客户端请求，通过异步非阻塞的方式处理I/O操作，可以提高系统的性能和吞吐量。

3. **快速的V8引擎**: Node.js基于Google Chrome浏览器中使用的V8引擎，这是一个快速的JavaScript引擎，能够快速地执行JavaScript代码。

4. **轻量级和高效**: Node.js本身非常轻量级，因此可以快速启动和运行，并且对系统资源的消耗相对较低。

5. **NPM（Node Package Manager）**: Node.js配备了一个强大的包管理工具NPM，可以方便地安装、更新、卸载Node.js模块，使得开发过程更加便捷。

6. **生态系统丰富**: Node.js拥有庞大的生态系统，有大量的第三方模块和库可以使用，从而大大提高了开发效率。

总的来说，Node.js是一个强大的后端开发工具，特别适合构建实时、高性能的网络应用程序，如Web服务器、API服务器、实时通讯应用等。

# nodejs发展历史

Node.js的发展历史可以追溯到2009年。以下是Node.js的主要发展历程：

1. **2009年：Node.js诞生**：
   - Node.js由Ryan Dahl在2009年创建，并于同年发布第一个版本。最初的目标是构建能够处理高并发、非阻塞I/O的网络应用程序。

2. **2010年：NPM的诞生**：
   - 2010年，Isaac Z. Schlueter创建了NPM（Node Package Manager），这是一个用于管理Node.js模块的包管理工具。NPM极大地促进了Node.js生态系统的发展。

3. **2011年：Node.js在企业中获得关注**：
   - 2011年，Node.js开始在企业界引起关注，许多公司开始尝试将Node.js用于构建高性能、实时的网络应用程序。这一年，Node.js发布了0.4.x、0.6.x和0.8.x等版本，持续改进和增强功能。

4. **2012年：Node.js进入企业级**：
   - 2012年，Node.js开始被更多的大型企业采用，并且得到了更广泛的支持和认可。社区开始致力于提高Node.js的稳定性和安全性。

5. **2013年：成立Node.js基金会**：
   - 2013年，Node.js基金会正式成立，旨在推动Node.js的发展、管理项目和社区，并促进Node.js在企业和开源社区中的持续增长。

6. **2014年至今：持续发展和壮大**：
   - 自2014年以来，Node.js一直在持续发展壮大。发布了一系列的稳定版本，不断改进性能、稳定性和安全性。Node.js生态系统也不断丰富，拥有大量的第三方模块和工具，使得Node.js成为一个强大的后端开发平台。

总的来说，Node.js经过多年的发展，已经成为构建高性能、实时的网络应用程序的首选技术之一，在企业和开源社区中都拥有广泛的影响力和支持。

# nodejs有哪些不足

尽管Node.js在构建高性能、实时的网络应用方面具有许多优势，但它也存在一些不足之处。以下是一些常见的Node.js的不足之处：

1. **单线程限制**：尽管Node.js采用了事件驱动的异步I/O模型，但其单线程的特性也带来了一些限制。特别是在处理CPU密集型任务时，单线程模型可能会导致性能瓶颈。

2. **回调地狱（Callback Hell）**：在复杂的异步代码中，使用回调函数会导致代码嵌套层级过深，使得代码难以理解和维护，这被称为“回调地狱”。

3. **缺乏统一的标准库**：与其他一些语言和框架相比，Node.js的标准库相对较小，缺乏一些常见功能的内置支持，这可能需要依赖第三方模块。

4. **稳定性和性能问题**：尽管Node.js在大多数情况下表现良好，但在某些情况下可能会出现内存泄漏、性能下降或者崩溃的情况，这需要开发者密切关注和处理。

5. **异步编程复杂性**：尽管Node.js的异步编程模型提供了高效的I/O操作，但对于一些开发者来说，理解和管理异步代码可能具有一定的挑战性，特别是对于初学者来说。

6. **生态系统的不稳定性**：虽然Node.js拥有庞大的生态系统，但其中一些模块可能缺乏更新和维护，导致依赖不稳定或者存在安全风险。

7. **不适用于CPU密集型任务**：由于Node.js的单线程模型以及JavaScript的特性，它并不适合用于处理大量的CPU密集型任务，这会导致性能下降。

尽管存在这些不足之处，但Node.js仍然是一个非常强大和受欢迎的后端开发平台，很多开发者仍然喜欢使用它来构建高性能的网络应用程序。



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

## 创建Buffer

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

使用buf.toString函数。

```

```

# Stream

Stream是一个抽象接口。

Node中很多对象实现了这个接口。

Stream有4种类型：

1、Readable。

2、Writable。

3、Duplex。可读写。

4、Transform。操作被写入数据，然后读出结果。

所有Stream对象都是EventEmitter的实例。常用的事件有：

1、data。当有数据可读时触发。

2、end。没有更多数据可读时触发。

3、error。读写过程出错时触发。

4、finish。数据写入完成时触发。

##读取流

```
var fs = require("fs");
var data = '';

var readerStream = fs.createReadStream("input.txt");

readerStream.setEncoding("UTF8");
readerStream.on('data', function(chunk) {
	data += chunk;
});

readerStream.on('end', function() {
	console.log(data);
});

readerStream.on('error', function(err) {
	console.log(err,stack);
});

console.log("end of code");

```

## 写入流

## 管道流

## 链式流



# 模块系统

文件和模块是一一对应的。

也就是说，一个node.js文件就是一个模块。

对应的2个对象是：

1、exports。模块公开的接口。

2、require。从外部获取一个模块的接口。











# 参考资料

1、node.js教程

http://www.runoob.com/nodejs





