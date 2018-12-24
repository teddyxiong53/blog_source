---
title: nodejs之全局对象
date: 2018-12-22 10:40:17
tags:
	- nodejs
---



js里有一个特殊的对象，叫做全局对象。

全局对象可以在程序的任何地方访问到。

在浏览器的js里，通常windows是全局对象。

而在nodejs里，全局对象是global。所有全局变量都是global的属性。



global的最根本的作用是作为全局变量的宿主。

根据ECMAScript的定义，满足以下条件的变量是全局变量。

1、最外层定义的变量。

2、全局变量的属性。

3、隐式定义的变量。没有定义直接赋值的就是。



一定要用var定义变量，以免不小心引入全局变量。因为全局变量会污染命名空间。

常用的全局变量有：

```
__filename
__dirname
setTimeout(cb, ms)
clearTimeout(t)，t是setTimeout得到的句柄。
setInterval(cb, ms)和setTimeout的区别是，这个是反复执行的。
console
process：这个最复杂，也很有用。下面详解看看。
```



process的常用事件：

```
exit
beforeExit
uncaughtException
Signal
```

举例：

```
process.on('exit', function(code) {
	setTimeout(function() {
		console.log("never happen")
	}, 0)
	console.log('exit code is: ' + code)
});
console.log("execute finish")
```

process的常用属性：

```
stdint/stdout/stderr
argv
execPath
```

演示如下：

```
//argv: D:\nodejs\node.exe,D:\work\test\test.js
console.log("argv: " + process.argv)
//execPath: D:\nodejs\node.exe
console.log("execPath: " + process.execPath)
//empty
console.log("execArgv: " + process.execArgv)

//打印所有环境变量
console.dir(process.env)
//v10.14.2
console.log(process.version)

//会打印依赖的版本库
console.log(process.versions)

//配置
console.log(process.config)

//4732 'test' 'x64' 'win32'
console.log(process.pid, process.title, process.arch, process.platform, process.mainModule)

```

常用方法

```
abort：会退出，打印堆栈。
chdir
cwd
exit

```

演示：

```
process.chdir("d:\\work")
console.log(process.cwd())
```











参考资料

1、Node.js 全局对象

http://www.runoob.com/nodejs/nodejs-global-object.html







