---
title: nodejs之工具模块
date: 2018-12-24 15:32:17
tags:
	- nodejs
---



提供了os的操作函数。

13个函数。

```
var os = require('os')
var util = require('util')
console.log("os.tmpdir: " + os.tmpdir() + "\n"
	+ "os.endianness: " + os.endianness() + "\n"
	+ "os.hostname: " + os.hostname() + "\n"
	+ "os.type: " + os.type() + "\n"
	+ "os.platform: " + os.platform() + "\n"
	+ "os.release: " + os.release() + "\n"
	+ "os.uptime: " + os.uptime() + "\n"
	+ "os.loadavg: " + os.loadavg() + "\n"
	+ "os.totalmem: " + os.totalmem() + "\n"
	+ "os.freemem: " + os.freemem() + "\n"
	+ "os.cpus: " + util.inspect(os.cpus()) + "\n"
	+ "os.networkinterfaces: " + util.inspect(os.networkInterfaces())
	)
```

```
λ  node test.js
os.tmpdir: C:\Users\ADMINI~1\AppData\Local\Temp
os.endianness: LE
os.hostname: doss
os.type: Windows_NT
os.platform: win32
os.release: 6.1.7601
os.uptime: 23965
os.loadavg: 0,0,0
os.totalmem: 8465620992
os.freemem: 1928851456
```



path模块

```
path.normalize("./")：规范化路径。
path.join("./", "test")
path.resolve([from ...], to)把to参数解析为绝对路径。从右往左，直到可以形成一个绝对路径。
```

```
var path = require("path")

console.log(path.resolve("d:/work", "test"))
//这个得到d:/nodejs，因为已经是一个绝对路径了。
console.log(path.resolve("d:/work", "d:/nodejs"))
```



参考资料

1、Node.js OS 模块

http://www.runoob.com/nodejs/nodejs-os-module.html

