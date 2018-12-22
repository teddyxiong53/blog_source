---
title: nodejs基本语法
date: 2018-12-22 14:59:17
tags:
	- nodejs

---



js是脚本语言，脚本语言都需要一个解释器。

对于嵌入在网页里的js脚本，浏览器充当了解释器的角色。

对于独立运行的js，nodejs充当了解释器的角色。

每一种解释都是一个运行环境，不但允许js定义各种数据结构，进行各种计算，还允许js用运行环境内置的对象和方法做一些事情。

例如，运行在浏览器里的js，主要用途是操作dom对象。浏览器就提供了document这些内置对象。

而在nodejs里，主要是操作磁盘文件或者搭建http服务，所以就提供了fs、http等对象。

nodejs的作者说，他创造nodejs的主要目的是实现高性能服务器，他看重的是事件机制和异步io模型的优越性，而不是js。

他需要一种语言，这种语言不能自带io功能，而且需要对事件机制有良好的支持。所以就选择了js。



因为参考的文章信息非常密集，我把很多内容单独写成文章了。

fs操作

简单的拷贝。

```
var fs = require("fs");
function copy(src, dst) {
	fs.writeFileSync(dst, fs.readFileSync(src));
}

function main(argv) {
	copy(argv[0], argv[1]);
}

main(process.argv.slice(2));
```

执行：

```
D:\work\test
λ  node .\test.js mod.js mod1.js
```

slice(2)，表示从argv[2]开始算。因为argv[0]是node，argv[1]是主模块的名字。

上面这个拷贝程序，拷贝小文件没有文件，大文件的话，可能把内存撑爆。

所以需要改进一下。用管道流过去。

```
function copy(src, dst) {
	fs.createReadStream(src).pipe(fs.createWriteStream(dst));
}
```





# 参考资料

1、七天学会NodeJS

http://nqdeng.github.io/7-days-nodejs/