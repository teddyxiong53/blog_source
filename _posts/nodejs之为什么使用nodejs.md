---
title: nodejs之为什么使用nodejs
date: 2019-04-15 15:28:28
tags:
	 - nodejs
---



既然我们已经有了php、java、python这些后端语言，我们为什么还需要nodejs？

nodejs适用于以下场景：

```
1、实时性应用。例如多人协作工具、网页聊天应用。
2、io密集型。
3、流式应用。例如客户端经常上传文件。
4、前后端分离。
```

缺点：

```
1、不适合cpu密集型应用。
```



当C10K问题提出来的时候，我们还在用Apache服务器。它的工作原理是fork一个进程来处理一个请求。

在fork的进程里处理php脚本。

后来Apache使用了fast cgi，这个本质上是一个进程池，减少了进程创建的时间，但是还是慢。

java的servlet使用了线程池。但是多线程编程的同步问题是个大麻烦。



如果不使用线程，还有两种解决方案：

1、使用协程coroutine。

2、非阻塞io。

nodejs就是使用的非阻塞io。



nodejs的线程模型

很多文章都说nodejs是单线程的。这种提法不太准确，因为至少我们会有这些疑问：

1、nodejs在一个线程里如何处理并发请求？

2、nodejs在一个线程里如何进行文件的异步io？

3、nodejs如何利用服务器上的多个cpu？

```
var http = require("http");
http.createServer(function(request, response) {
  response.end("hello world\n");
}).listen(8888);

console.log("server running on 8888");
```



因为nodejs是基于事件的，当我们有网络访问事件产生时，它的回调函数才会执行。

当有多个请求到来时，它们会排成队列，一个个依次执行。

回调函数是同步执行的，如果回调很慢，那就会严重影响性能。

我们可以做一个实验。

```
var http = require("http");
var output = require("./string")

http.createServer(function(request, response) {
  output.output(response);
}).listen(8888);

console.log("server running on 8888");
```

当前目录写一个string.js文件。

```
function sleep(ms) {
    var startTime = new Date().getTime();
    while(new Date().getTime() < startTime + ms);
}

function outputString(resp) {
    sleep(10*1000);
    resp.end("hello world\n");
}

exports.output = outputString;
```

访问地址，可以看到，要等10秒才能得到返回网页。



异步是为了优化体验，避免卡顿。

而真正节省处理时间，利用cpu多核性能，还是要靠多线程。

实际上nodejs底层维护了一个线程池。

线程池里默认有4个线程，用来进行文件io。

不过，我们无法控制到这个线程池，所以不需要关心它。



如果有少量的cpu密集型任务要处理，我们可以启动多个nodejs进程来做，并用进程间通信。

如果有大量的cpu密集型任务，那么使用nodejs就是一个错误。







参考资料

1、为什么要用 Node.js

http://blog.jobbole.com/100058/?utm_source=blog.jobbole.com&utm_medium=relatedPosts