---
title: js之promise
date: 2018-12-25 16:37:55
tags:
	- js

---

1

代码可以看到shadownode里的promise.js的实现。只有300行代码。

是从这个弄过来的。

https://github.com/taylorhakes/promise-polyfill



本来是在js之异步编程里讨论这个的。

N-blog的教程里提到有网友专门写了一本小书来讨论这个东西，看来这个里面的水是很深的。所以我单独拉一篇文章来学习。

先看一个简单例子。

```
Promise.resolve().then(()=> {
    return new Promise((resolve, reject)=> {
        setTimeout(function() {
            console.log("1111");
            resolve("1 - resolve");
        }, 2000);
    })
}).then(()=> {
    console.log("222");
})
```

这个是演示promise的串联的。

这个是异常的。还把错误传递过去了。

```
Promise.resolve().then(()=> {
    return new Promise((resolve, reject)=> {
        setTimeout(function() {
            console.log("1111");
            reject("xxxxxxxx");//这里带参数
        }, 2000);
    })
}).then(()=> {
    console.log("222");
}).catch((e)=>{
    console.log("get reject");
    console.log("err msg:" + e);
})
```

看看resolve传递参数的。

```
Promise.resolve().then(()=> {
    return new Promise((resolve, reject)=> {
        setTimeout(function() {
            console.log("1111");
            resolve(111);
        }, 2000);
    })
}).then((value)=> {
    console.log("get val from resolve " + value);
    console.log("222");
}).catch((e)=>{
    console.log("get reject");
    console.log("err msg:" + e);
})
```







# 什么是Promise？

一个Promise对象表示一个目前还不可用，**但是在未来的某个时间点可以被解析的值。**

它允许你以同步的方式编写异步代码。

Promise把之前嵌套的回调函数，用then穿起来了。

代码看起来清晰多了。





我们在浏览器的console里，用这个查看一下：

```
console.dir(Promise)
```

可以看到：

1、Promise是一个构造函数。

2、自己有all、reject、resolve这些函数。

3、它的原型有then、catch方法。

新建app.js。

里面写这些：

```
var p = new Promise(function(resolve, reject) {
	setTimeout(function() {
		console.log("执行完成");
		resolve("随便什么数据");
	}, 2000);
});
```

执行：node app.js。

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ node app.js 
执行完成
```

我们要注意，我们只是new了一个对象，并没有执行什么，为什么会运行呢？

所以我们一般是这样用的。用函数把对象包起来。

```
function runAsync() {
	var p = new Promise(function(resolve, reject) {
		setTimeout(function() {
			console.log("执行完成");
			resolve("随便什么数据");
		}, 2000);
	});
	return p;
}

runAsync();
```

我们看看包装后的函数。

这样一个函数有什么用呢？

我们包装的函数，返回了一个Promise对象。

**这个对象可以执行then和catch函数。**

```
runAsync().then(function(data) {
	console.log(data);
});
```

运行效果是这样：

```
执行完成
随便什么数据
```

then里可以取到resolve的参数。

then达到的效果，跟普通的回调函数类型。

但是写起来要清晰很多。

所有接口：

```
原型方法：3个
Promise.prototype.catch 
	其实是调用了then。
Promise.prototype.then 
	返回了一个promise。
Promise.prototype.finally
	调用了then。所有也是返回了promise对象。
	
	
类方法
Promise.all
	也是返回了一个promise。先把所有的promise执行。
Promise.resolve 
	也是返回promise。
Promise.reject
Promise.race

总结：所有的promise方法，都是返回了promise对象。这样是为了进行链式调用。
```



`Promise.resolve()`用于将现有对象转换为`Promise`对象，从而控制异步流程。

而立即`resolve`的`Promise`对象是在本轮“事件循环”（Event loop）的结束时，而不是在下一轮“事件循环”的开始时。

看js代码的时候，我们要时刻意识到，我们写的代码，是在这样一个死循环里运行的。

```
while(true) {
	//我们看到的js代码
}
```



下面的代码运行过程值得注意。

```
setTimeout(function () {
    console.log('three');
}, 0);

Promise.resolve().then(function () {
    console.log('two');
});

console.log('one');

// one
// two
// three

```



自己写的例子。

```
var console = require('console')
Promise.resolve().then(()=> {
    return new Promise((resolve, reject) => {
        setTimeout(()=> {
            console.log("timeout")
            resolve(111) //如果这里不resolve的话，后面就不会执行。
        },2000)
    })
}).
then(()=> {
    return checkOta()
}).then(()=> {
    return checkAuth()
}).then(()=> {
    console.log("end promise")
}).catch((e) => {
    console.log("catch" + e)
})

function checkOta() {
    return new Promise((resolve)=>{
        console.log("in ota")
        resolve("ota")
    })
}
function checkAuth() {
    return new Promise((resolve, reject)=> {
        console.log("in auth")
        // resolve("auth")
        reject("auth")
    })
}
console.log("end of code")
```



参考资料

1、理解 Promise 的工作原理

https://blog.coding.net/blog/how-do-promises-work

2、Promise详解与实现（Promise/A+规范）

https://zhuanlan.zhihu.com/p/32913092

3、Promise对象是用来干嘛的?

https://blog.csdn.net/Wbiokr/article/details/79490390

4、Promise.resolve()

https://www.jianshu.com/p/3bd1c6865bba