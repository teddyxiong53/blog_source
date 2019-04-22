---
title: js之promise
date: 2018-12-25 16:37:55
tags:
	- js

---



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



我通过vscode看看Promise的定义。

只有2个方法。

```
interface Promise<T> {
	then
	catch
}
```

#什么是Promise？

一个Promise对象表示一个目前还不可用，但是在未来的某个时间点可以被解析的值。

它允许你以同步的方式编写异步代码。

Promise把之前嵌套的回调函数，用then穿起来了。

代码看起来清晰多了。



#Promise A规范

Promise表示一个最终值。这个值有一个操作完成时返回。

Promise有三种状态：

```
1、未完成。
2、完成。
3、失败。
```

Promise只能从从未完成转换到完成，或者从未完成转换到失败。

这个转换只发生一次。

Promise有一个then方法，这个方法接受3个函数做参数。

```
1、完成时的回调。
2、失败时的回调。
3、进度信息回调。
```

# Promise B规范





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

这个对象可以执行then和catch函数。

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



参考资料

1、理解 Promise 的工作原理

https://blog.coding.net/blog/how-do-promises-work

2、Promise详解与实现（Promise/A+规范）

https://zhuanlan.zhihu.com/p/32913092

3、Promise对象是用来干嘛的?

https://blog.csdn.net/Wbiokr/article/details/79490390