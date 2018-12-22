---
title: js之require、import、export
date: 2018-12-19 11:15:17
tags:
	- js

---



#require

require，后面跟的模块名，js后缀可以省略。

可以是绝对路径、相对路径等。

除了js模块，还可以用require来加载一个json文件。

```
var data = require("./data.json");
```



# exports

exports对象是当前模块的导出对象。

用于导出模块公共方法和属性。

别的模块通过require得到就是当前模块的exports对象。

mod.js

```
exports.hello = function() {
	console.log("hello world");
}
```

test.js

```
var mod = require("./mod.js");

mod.hello();
```

# module

主要用途是替换当前模块的导出对象。

模块默认导出的是一个对象，可以替换为一个函数。

上面的例子可以改为下面这样。

```
module.exports = function() {
	console.log("hello world");
}
```



```
var mod = require("./mod.js");

mod();
```



#模块的初始化

一个模块里的js代码只在第一次被使用的时候执行一次。并在执行过程中初始化模块的导出对象。

之后，缓存起来的导出对象会被反复利用。



# 主模块

传递给node的js文件，就是主模块。



# 二进制模块

后缀是node。

用得少。



#参考资料

1、一文让你彻底搞清楚javascript中的require、import与export

https://www.jb51.net/article/124442.htm

2、NodeJS基础

http://nqdeng.github.io/7-days-nodejs/