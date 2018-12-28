---
title: js之Array.prototype.slice.apply
date: 2018-12-22 10:25:17
tags:
	- js
---



看代码看到js之Array.prototype.slice.apply这一串东西。

具体是什么含义呢？



Array是js里的基本数据类型，你可以用Array.prototype获取它的属性。

```
console.log(Array.prototype);
```

得到的结果是这样的：

```
concat: ƒ concat()
constructor: ƒ Array()
copyWithin: ƒ copyWithin()
entries: ƒ entries()
every: ƒ every()
...
```

slice是js的一个方法，用来从数组里取出一部分数据。并返回一个新的数组。

它可以接收2个参数；startIndex（必须的）和endIndex（可选的）。

举例：

```
var a = ["a", "b", "c"];
b = a.slice(1,2);
console.log(b);
```



```
function f(a,b) {
	return arguments;
}
console.log(Array.prototype.slice.apply(f("1", "2")) instanceof Array); 
```



一个完整例子。

```
const EventEmitter = require("events");

class BufferManager extends EventEmitter {
	
	constructor() {
		super();
		this._buffer = Array.prototype.slice.apply(arguments).filter(function(a) {
			return Buffer.isBuffer(a);
		});
	}
}

var bufferManager = new BufferManager(1);
console.log(bufferManager._buffer);
var buffer = Buffer.alloc(10);
var bufferManager2 = new BufferManager(buffer);
console.log(bufferManager2._buffer);
```

运行结果：

```
D:\work\test
λ  node .\test.js
[]
[ <Buffer 00 00 00 00 00 00 00 00 00 00> ]
```





# 简单例子

```
class MyClass {
    constructor() {
        this._buffers = Array.prototype.slice.call(arguments).filter(function() {
            return true;
        });
    }
}


var c1 = new MyClass(1,2);
console.log(typeof c1._buffers);
console.log(c1._buffers);

var c2 = new MyClass("abc");
console.log(c2._buffers);
```

输出：

```
object
[ 1, 2 ]
[ 'abc' ]
```



# 参考资料

1、理解 JavaScript 中的 Array.prototype.slice.apply(arguments)

https://blog.csdn.net/u013565133/article/details/70853214