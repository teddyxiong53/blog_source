---
title: webbench代码分析
date: 2019-02-20 11:49:08
tags:
	- 网络
---





代码在这里。

https://github.com/EZLippi/WebBench

直接make就好了。

作者的官网，写了不少的软件。

http://home.tiscali.cz/~cz210552/index.html

运行：

```
hlxiong@hlxiong-VirtualBox ~/work/study/WebBench (master*) $ ./webbench http://www.baidu.com/
Webbench - Simple Web Benchmark 1.5
Copyright (c) Radim Kolar 1997-2004, GPL Open Source Software.

Request:
GET / HTTP/1.0
User-Agent: WebBench 1.5
Host: www.baidu.com


Runing info: 1 client, running 30 sec.

Speed=460 pages/min, 1188316 bytes/sec.
Requests: 230 susceed, 0 failed.
```



```
hlxiong@hlxiong-VirtualBox:~/work/study/WebBench$ ./webbench http://localhost/
Webbench - Simple Web Benchmark 1.5
Copyright (c) Radim Kolar 1997-2004, GPL Open Source Software.

Request:
GET / HTTP/1.0
User-Agent: WebBench 1.5
Host: localhost


Runing info: 1 client, running 30 sec.

Speed=542516 pages/min, 2278567 bytes/sec.
Requests: 271258 susceed, 0 failed.
```



是构造了一个request字符串。直接对socket进行write操作和read来做的。

