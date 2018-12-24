---
title: nodejs之模块系统
date: 2018-12-24 14:00:17
tags:
	- nodejs
---





为了让nodejs的文件可以相互调用。

nodejs提供了一个简单的模块系统。

模块是nodejs应用的基本组成部分，文件和模块是一一对应的。

也就是说，一个nodejs文件，就是一个模块。

这文件可能是：

1、js代码。

2、json文件。

3、c或者c++扩展。

导出方式有2种：

```
exports.myfunc = function() {
    
}
```

下面这种是把对象封装到模块里了。

```
module.exports = function() {
    
}
```

使用上，看看有什么不一样。

第一种方式：

test.js

```
var mod = require("./mod")
mod.myfunc()
```

mod.js

```
exports.myfunc = function() {
	var name = "XX"
	console.log("hello " + name)
}
```



第二种方式：

test.js

```
var mod = require('./mod')
m = new mod()
m.sayName()
```

mod.js

```
module.exports = function() {
	var name = 'xx'
	this.sayName = function() {
		console.log('hello ' + name)
	}
	console.log("use module.exports")
}
```

第二种方式，还需要new，第一种方式，不需要new。



参考资料

1、Node.js模块系统

http://www.runoob.com/nodejs/nodejs-module-system.html