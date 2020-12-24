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



# 我的思考

可以统一用第二种方式。

第二种方式，确实也有两种情况。

1、输出对象。

2、输出类。

输出对象的情况。

config.js

```
module.exports = {
    name : "xhl"
};
```

test.js

```
cfg = require("config.js");
console.log(cfg.name);
```

输出类的情况。

myclass.js

```
class MyClass {
    
}
module.exports = MyClass;
```

test.js

```
MyClass = require("myclass");
myClass = new MyClass();
```

还可以在一个文件导出多个符号。

```
module.exports.func1 = func1;
module.exports.func2 = func2;
```





参考资料

1、Node.js模块系统

http://www.runoob.com/nodejs/nodejs-module-system.html