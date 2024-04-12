---
title: js之promise
date: 2018-12-25 16:37:55
tags:
	- js

---

--

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

看js代码的时候，我们要时刻意识到，我们写的代码，是在这样一个死循环里运行的。（要有注册事件监听，如果没有一个事件注册监听的，那么就会break退出了）

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

# promisify



https://juejin.cn/post/7000026472832319495

对于有返回值的函数，用promisify还比较好理解。

但是对于setTimeout，promisify之后，是个什么情况呢？

setTimeout的直接就是延时的效果。我把本来应该放到回调里的函数，直接放在延时的后面手动调用就好了。

就等价于delay ms一样。

```
setTimeoutAsync = promisify(setTimeout)

// var delay1 = function (ms) {
//     return new Promise(resolve => setTimeout(resolve, ms))
// }
async function test () {
    console.log('before')
    // await delay1(1000)
    var res = await setTimeoutAsync(1000)
    //本来的回调放这里。
    myfunc()
    console.log(`after, res:${res}`)
}
```

那对setInterval又是什么情况呢？

这个需要多加一下封装代码才能达到效果。

# 回调的promise化

我看yodajs里，基本所有的接口都是返回promise，这就是所谓的promise化，那么这样带来的好处是什么？

又有什么需要注意的地方呢？

不得不面对的现实是仍然有大量的老旧的采用回调的方式的函数，

如果你在业务开发中受不了了，

那么就可以考虑一下 Promise 化你的 callback 调用

其实我们仔细想想，最简陋的方式就是用一个 Promise 包装一下，

自己实现的promisify函数如下：

```js
const promisify = (fn) => (...args) => new Promise((resolve, reject) => {
        args.push(resolve)
        fn.apply(this, args)
    })
```

**将 resolve 替换为 callback 传给原函数就可以了**，

如下：

```
var testCb = function (a, b, callback) {
	setTimeout(()=> {
		callback(a,b)
	}, 1000)
}

promisify(testCb)(10,20).then(data=> {
	console.log(data)
})
```



或许你的函数设计者受 Node.js api 的影响，

会将 `error` 对象作为 `callback` 的第一个参数，

那么我们只需要将 `error` `reject` 就可以了

```
const promisify = (fn) => (...args) => new Promise((resolve, reject) => {
    args.push((err, ...result) => {
        if (err) reject(err)
        else resolve.apply(this, result)
    })
    fn.apply(this, args)
})
```



现在的JS异步编程，通常都会使用async/await模式，但要支持这个模式,await后面必须是一个Promise对象。
因而对于现存的很多基于回调模式的API，我们需要将其Promise化来实现“类同步”调用。



异步调用的问题：我不知道什么时候调用完成
解决方案：

1. 你调用完成后帮我执行剩下的逻辑
2. 你调用完成后告诉我，我自己执行剩下的逻辑



第二种方式更有利于将异步过程同步化，

毕竟对我来说要做的就是等待然后执行下面的逻辑

要实现“你调用完成告诉我”，

我们需要一个中间容器**接收这个“信号”和返回值，**

Promise就是这个容器

要实现将回调**Promise化**，

**本质**就是在回调函数中将“调用方”传入的参数(返回值)和调用完成的**“信号”存入Promise容器**

**在JS中由于闭包的存在**，任何地方执行回调函数都能够影响外部变量，

因而可以方便的更改Promise的状态，实现Promise化



实现对setTimeout的promise化

```
function PromiseSetTimeout(handler, timeout) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            handler()
            resolve()  // 核心就是这一步
        }, timeout)
    })
}
```

调用这样：

```
PromiseSetTimeout(() => {
    console.log("time out");
}, 2000).then(data => {
    console.log("then function after 2000ms");
})
```

用async的方式调用

```
async function test() {
    const ret = await PromiseSetTimeout(() => {
        console.log("time out");
    }, 2000)
    console.log("then function after 2000ms")
}
 
test()
```



参考资料

1、

https://cloud.tencent.com/developer/article/1470718

2、

https://www.cnblogs.com/Peter2014/p/13023368.html



# 简介

当谈到JavaScript中的异步编程时，Promise是一个非常重要的概念。Promise是一种用于处理异步操作的对象，它表示一个异步操作的最终完成（或失败）及其结果的值。

以下是Promise的一些关键特点和用法：

1. **状态（State）**：
   - Promise有三种状态：pending（进行中）、fulfilled（已成功）和rejected（已失败）。
   - 当一个Promise被创建时，它的初始状态是pending。
   - 当操作成功完成时，Promise的状态变为fulfilled，并且会调用`then`方法的成功处理函数。
   - 当操作失败时，Promise的状态变为rejected，并且会调用`catch`方法或`then`方法的失败处理函数。

2. **创建Promise**：
   - 使用`new Promise()`来创建一个Promise对象。它接受一个带有两个参数的函数作为参数，分别是resolve和reject。resolve用于将Promise状态从pending变为fulfilled，而reject用于将Promise状态从pending变为rejected。
   - 示例：`const myPromise = new Promise((resolve, reject) => { /* 异步操作 */ });`

3. **Promise链**：
   - 可以通过串联多个Promise来处理复杂的异步操作。这就是所谓的Promise链。
   - 使用`then`方法来连接Promise。每个`then`方法都返回一个新的Promise对象，使得可以在Promise链中进行进一步的操作。
   - 示例：`myPromise.then(onFulfilled, onRejected).then(onFulfilled2, onRejected2);`

4. **错误处理**：
   - 可以使用`catch`方法来捕获Promise链中任何Promise的rejected状态，并进行错误处理。
   - 示例：`myPromise.catch(onRejected);`

5. **Promise.all和Promise.race**：
   - `Promise.all(iterable)`接受一个可迭代对象（比如数组）作为参数，返回一个新的Promise，在所有Promise都成功时才会成功，否则失败。
   - `Promise.race(iterable)`同样接受一个可迭代对象作为参数，但只要有一个Promise成功或失败，它就会返回一个成功或失败的新Promise。
   - 示例：`Promise.all([promise1, promise2, promise3]);` 或 `Promise.race([promise1, promise2, promise3]);`

Promise在JavaScript中广泛用于处理异步操作，它提供了一种更优雅和可维护的方式来编写和管理异步代码。

# 用贴合实际的例子来说明async和await的用法

当涉及到异步操作时，`async`和`await`是JavaScript中更现代、更清晰的异步编程方式。下面是一个简单的例子来说明它们的用法，假设我们有一个获取用户信息的异步函数`getUserInfo()`：

```javascript
// 异步函数，模拟获取用户信息
function getUserInfo(userId) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (userId === 1) {
                resolve({ id: 1, username: 'exampleUser' });
            } else {
                reject(new Error('User not found'));
            }
        }, 1000);
    });
}

// 使用 async/await 处理异步操作
async function fetchUserInfo(userId) {
    try {
        const userInfo = await getUserInfo(userId);
        console.log('User info:', userInfo);
        return userInfo;
    } catch (error) {
        console.error('Error fetching user info:', error.message);
        throw error;
    }
}

// 调用 async 函数
fetchUserInfo(1)
    .then((userInfo) => {
        console.log('User info fetched successfully:', userInfo);
    })
    .catch((error) => {
        console.error('Failed to fetch user info:', error.message);
    });
```

在上面的例子中，我们首先定义了一个异步函数`getUserInfo()`，用于模拟获取用户信息的操作。然后，我们使用`async function fetchUserInfo()`定义了另一个异步函数，它使用`await`关键字等待`getUserInfo()`函数返回结果。使用`await`关键字能够使异步代码看起来更像同步代码，提高了代码的可读性。

在`fetchUserInfo()`函数中，我们使用`try...catch`语句来捕获可能发生的错误。如果`getUserInfo()`函数返回成功，则`await`会返回一个包含用户信息的对象，并打印到控制台。如果`getUserInfo()`函数返回失败，则会抛出一个错误，被`catch`捕获，然后打印错误信息到控制台。

最后，我们调用`fetchUserInfo(1)`函数来获取id为1的用户信息。在`then`方法中，我们处理成功的情况，打印用户信息；在`catch`方法中，我们处理失败的情况，打印错误信息。

# 参考资料

1、理解 Promise 的工作原理

https://blog.coding.net/blog/how-do-promises-work

2、Promise详解与实现（Promise/A+规范）

https://zhuanlan.zhihu.com/p/32913092

3、Promise对象是用来干嘛的?

https://blog.csdn.net/Wbiokr/article/details/79490390

4、Promise.resolve()

https://www.jianshu.com/p/3bd1c6865bba

5、

https://juejin.cn/post/7042190759730085918