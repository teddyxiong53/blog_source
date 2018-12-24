---
title: nodejs之文件操作
date: 2018-12-24 15:09:17
tags:
	- nodejs
---



nodejs提供一组posix标准的文件操作api。

fs模块所有函数都有2个版本：同步和异步。建议用异步版本。

默认的都是异步的，同步的函数名后面跟了Sync。

```
var fs = require('fs')

fs.readFile('1.txt', function(err, data) {
	if(err) {
		return console.error(err);
	}
	console.log("async read: ", data.toString())
})

var data = fs.readFileSync('1.txt')
console.log("sync read: " + data.toString())

console.log("end of code")
```



文件操作：

```
打开
fs.open(path, flag[,mode], callback)
查询信息
fs.stat(path, callback)
写入
fs.writeFile
读取
fs.readFile
关闭
fs.close
截取
fs.truncate(fd, len, callback)
删除
fs.unlink(path, callback)
```

目录操作：

```
创建
fs.mkdir(path[,path], callback)
读取目录
fs.readdir(path, callback)
删除目录
fs.rmdir(path, callback)

```



参考资料

1、Node.js 文件系统

http://www.runoob.com/nodejs/nodejs-fs.html