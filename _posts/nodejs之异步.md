---
title: nodejs之异步
date: 2018-12-19 14:49:17
tags:
	- nodejs

---



实现异步的方式有：

1、回调。

2、事件。

3、promise和async、await。

#回调

回调是最简单，最容易理解的方式。

先看一个简单例子。

```
var i = 0;
function sleep(ms, callback) {
	setTimeout(function() {
		console.log("I execute ok");
		i++;
		if(i>=2) {
			callback(new Error("i > 2 now", null));
		} else {
			callback(null, i);
		}
	}, ms);
}

sleep(3000, function(err, val) {
	if(err) {
		console.log("err happens: " + err.message);
	} else {
		console.log(val);
	}
});
```

这个看起来好像也没有什么不妥的。

但是如果要暂停多次，那么写起来就是这个样子，看起来很反人类。

```
sleep(1000, function(err, val) {
	if(err) {
		return console.log(err.message);
	}
	console.log(val)
	sleep(1000, function(err, val) {
		if(err) {
			return console.log(err.message);
		}
		console.log(val);
	})
})
```

那么能够怎么改进呢？

我们可以把多次暂停看成多个异步任务。

可以用事件监听的方式来做。每次调用一个异步函数，都返回一个EventEmitter对象。并在执行成功的时候，调用done事件。在失败的时候，调用error事件。

```
const Emitter = require('events')
var i = 0

function sleep(ms) {
	var emitter = new Emitter()
	setTimeout(function() {
		console.log('I finish my work')
		i++;
		if(i>=2) {
			emitter.emit('error', new Error('i > 2'))
		} else {
			emitter.emit('done', i);
		}
	}, ms)
	return emitter
}
var emit = sleep(3000)
emit.on('done', function(val) {
	console.log("success: " + val)
})

emit.on('error', function(err) {
	console.log('error: ' + err.message)
})
```

但是还是不够好。

更好的解决方案是用promise。

改写如下：

```
var i = 1
function sleep(ms) {
	return new Promise(function(resolve, reject) {
		setTimeout(function() {
			console.log("I have done my job")
			i++
			if(i > 2) {
				reject(new Error("i>2"))
			} else {
				resolve(i)
			}
		}, ms)
	})
}

sleep(1000).then(function(val) {
	console.log(val)
	return sleep(1000)
}).then(function(val) {
	console.log(val)
	return sleep(1000)
}).then(function(val) {
	console.log(val)
	return sleep(1000)
}).catch(function(err) {
	console.log("error happens: " + err.message)
})

```

执行结果：

```
D:\work\test
λ  node test.js
I have done my job
2
I have done my job
error happens: i>2
```

我们可以从这里看出，promise带来的好处：

1、把原来嵌套的回调函数展开了。代码看起来更加舒服了。

2、promise的冒泡性质，当promise链条里的任何一个函数出错都会直接抛出到链条的最底部。

所以我们统一用了一个catch去捕获。



但是promise只是解决了回调嵌套的问题，并没有解决回调本身的问题。

我们当前的代码仍然是用回调的。

所以还需要引入await和async关键字。

await和async在nodejs7版本开始支持。只是需要harmony（和谐）模式去运行。



async函数定义是这样：

```
async function func() {
    return 0;
}
```

在函数前面加上async就好了。

async函数的特征在于，调用return返回的不是一个普通的值，而是一个promise对象。

await只能在async函数里面用。

await后面要跟一个promise对象。

函数执行到await的位置，就退出该函数，直到事件轮询检查到promise有了状态resolve或者reject才执行执行该函数后面的内容。

```
var i = 1
function sleep(ms) {
	return new Promise(function(resolve, reject) {
		setTimeout(function() {
			console.log("I have done my job")
			i++
			if(i > 2) {
				reject(new Error("i>2"))
			} else {
				resolve(i)
			}
		}, ms)
	})
}

(async function() {
	try {
		var val
		val = await sleep(1000)
		console.log(val)
		val = await sleep(1000)
		console.log(val)
		val = await sleep(1000)
	} catch(e) {
		console.log("error happens: " + e.message)
	}
}())

```



# promise的用法

## Promise.all

```
var promise1 = Promise.resolve(3)
var promise2 = 42
var promise3 = new Promise(function(resolve, reject) {
	setTimeout(resolve, 100, 'foo')
})

Promise.all([promise1, promise2, promise3]).then(function(values) {
	console.log(values)
})

```

得到的结果是：

```
Array [3, 42, "foo"]
```



参考资料

1、node.js异步控制流程 回调，事件，promise和async/await

https://www.cnblogs.com/kazetotori/p/6043983.html

