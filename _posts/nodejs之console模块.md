---
title: nodejs之console模块
date: 2018-12-30 11:11:25
tags:
	- nodejs

---



console之前使用，都是一个console.log就完了。

其实，这个模块也有很多实用功能。

定义自己的console。

```
var mycon = new console.Console(process.stdout, process.stderr);
mycon.log("mycon");
```

重定向打印文件。

```
var fs = require("fs");
var output = fs.createWriteStream("./output.txt");
var error = fs.createWriteStream("./error.txt");
var mycon = new console.Console(output, error);
mycon.log("mycon stdout");
mycon.error("mycon error");
```

使用断言。

```
console.assert(false, "assert not pass");
```

测量执行时间。

```
console.time("aaa");
for(let i=0; i<1000; i++) {

}
console.timeEnd("aaa");
```

测量中间的时间。

```
console.time("aaa");
for(let i=0; i<3; i++) {
    console.timeLog("aaa");
}
console.timeEnd("aaa");
```





参考资料

1、

http://nodejs.cn/api/console.html

