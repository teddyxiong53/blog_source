---
title: js之async和await
date: 2019-04-22 16:03:25
tags:
	- js

---



async和await被称为是异步编程的终极解决方案。

内部实现都是用Promise实现的。

async用于声明一个函数为异步函数。

**await则是等待一个异步函数执行完成。**

async是一个修饰。

await是一个运算符。



async起什么作用？

这个问题的关键是，async函数怎么处理它的返回值。

写代码测试一下：

```
async function testAsync() {
	return "hello async";
}
var result = testAsync();
console.log(result);
```

运行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ node app.js 
Promise { 'hello async' }
```

可以看到，async函数返回的是一个Promise对象。

如果函数返回的是直接量，async会把这个直接量用Promise.resolve包装成Promise对象。

```
testAsync().then((v)=> {
	console.log(v);
})
```

**如果一个async修饰的函数没有返回值，那么得到的是什么？**

**是Promise.resolve(undefined)。**



await在等什么？

在等一个async函数完成。

await后面可以跟一个直接量，任意变量都可以。

```
function getSomething() {
    return "something";
}

async function testAsync() {
    return Promise.resolve("hello async");
}

async function test() {
    const v1 = await getSomething();
    const v2 = await testAsync();
    console.log(v1, v2);
}

test();
```

**如果await后面的不是一个Promise，那么await表达式的运算结果就是它等到的东西。**

如果await后面是一个Promise对象。

await会：

```
1、阻塞后面的代码。
2、等待Promise对象resolve。
3、得到resolve的结果。
```

await不会造成函数的阻塞。



单一的Promise链并不能看出async和await的优势。

多个Promise才能看出。



我们用setTimeout来模拟耗时的操作。

先看看不用await的情况。

```
function takeLongTime() {
	return new Promise(resolve=> {
		setTimeout(()=>resolve("long_time_value"), 1000);
	});
}
takeLongTime().then(v=> {
	console.log("got", v);
})
```

改成用async看看。

```
function takeLongTime() {
	return new Promise(resolve=> {
		setTimeout(()=>resolve("long_time_value"), 1000);
	});
}

async function test() {
	const v = await takeLongTime();
	console.log(v);
}

test();
console.log('end');
```

运行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ node app.js 
end
long_time_value
```

test函数并不会阻塞。所以end先打印。



我们看看多个then组成的逻辑链的情况。

假设一个业务，分成多个步骤完成，每一个步骤都是异步的。

仍然使用setTimeout来模拟耗时操作。

```
function takeLongTime(n) {
	return new Promise(resolve=> {
		setTimeout(()=>resolve(n+200), n);
	});
}

function step1(n) {
	console.log(`step1 with ${n}`);
	return takeLongTime(n);
}


function step2(n) {
	console.log(`step2 with ${n}`);
	return takeLongTime(n);
}

function step3(n) {
	console.log(`step3 with ${n}`);
	return takeLongTime(n);
}
//上面的公共函数部分。
function doIt() {
	console.time("doIt");
	const time1 = 300;
	step1(time1)
		.then(time2=> step2(time2))
		.then(time3 => step3(time3))
		.then(result => {
			console.log(`result is ${result}`);
			console.timeEnd("doIt");
		})
}
doIt();

```

我们看看用async来做。

```
async function doIt() {
	console.time('doIt');
	const time1 = 300;
	const time2 = await step1(time1);
	const time3 = await step2(time2);
	const result = await step3(time3);
	console.log(`result is ${result}`);
	console.timeEnd("doIt");
}
doIt();
```

看起来清晰多了。跟同步代码看起来几乎一样。



异步编程的方法，有这几种：

1、回调函数。

2、事件监听。

3、发布订阅。

4、Promise对象。



什么是异步？

异步就是把一个完整的任务分为两段，先执行第一段，然后执行其他任务，然后再回过头来执行任务的第二段。

例如，读取文件就是一个典型的耗时的异步行为。

我们用回调的方式来实现。

```
fs.readFile("1.txt", function(err, data) {
    if(err) {
        throw err;
    }
    console.log(data);
})
//继续执行其他任务。
```

开始读文件，是任务的第一段，读取完成，是任务的第二段。

**正是因为被拆成了两段，第一段跟第二段没法直接联系。**

所以nodejs约定了，回调函数的第一个参数是error对象，通过这个来把错误传递过来。



回调函数本身没有什么问题。

但是回调嵌套导致代码可读性变得很差。



Promise就是为了解决回调地狱而出现的。

**Promise的问题是大量冗余。**

**用这种方式写的代码，一眼看过去都是then。**



有没有更好的方式？

协程是一种。

协程有点像函数，又有点向线程。

它的执行流程是这样：

```
1、协程A开始运行。
2、协程A运行到一半，进入暂停，执行权转移到协程B。
3、协程B运行一段时间后，把控制权交还给协程A。
4、协程A继续运行。
```



读取文件的协程写法是这样：

```
function asyncJob() {
	//其他代码
    var f = yield readFile("1.txt");
    //其他代码
}
```

上面代码的关键就是yield关键字。

它把任务分为了两段。



Generator函数是协程在ES6的实现。

最大的特点就是可以交出函数的执行权。就是暂停。

一个简单的生成器函数是这样：

```
function *gen(x) {
    var y = yield x + 2;
    return y;
}
```

我们看这个函数的特点：

前面加了一个星号，来跟普通函数进行区别。

怎么来用呢？这个函数返回的是一个遍历器g。我们对遍历器调用next就可以了。

```
g = gen(1)
console.log(g.next())
console.log(g.next())
```

输出是这样：

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ node app.js 
{ value: 2, done: false }
{ value: undefined, done: true }
```

因为里面只有一个yield，所以调用一次next之后，就没有了。

如果有多个yield，就可以调用多次next。



async是什么？

async就是生成器函数的语法糖。

我们还是先看生成器函数，依次读取2个文件。

```
var readFile = function(fileName) {
    return new Promise(function(resolve, reject) {
        fs.readFile(fileName, function(error, data) {
            if(error) {
                reject(error);
            } else {
                resolve(data);
            }
        })
    })
}

var gen = function* () {
    var f1= yield readFile("1.txt")
    var f2 = yield readFile("2.txt")
    console.log(f1.toString())
    console.log(f2.toString())
}
var g= gen(1)
console.log(g.next())
console.log(g.next())
```

用async来实现，是这样的：

```
var asyncReadFile = async function() {
    var f1 = await readFile("1.txt")
    var f2 = await readFile("2.txt")
}
```

区别是什么？

就是

1、把星号换成了async，

2、把yield换成了await。



async函数的优点

1、内置执行器。只需要写一行就可以了。而生成器还需要用next调用。

2、更好的语义。

3、更广泛的适用性。



```
function sleep(n) {
    var start = Date.now();
    while(true) {
        if(Date.now() - start > n*1000) {
            break;
        }
    }
}
async function testAsync() {
    console.log("first part");
    await sleep(2);
    console.log('second part')
}

console.log("begin")
testAsync()
console.log("end")
```



用西红柿炒鸡蛋的过程来理解异步。

Promise相当于餐馆发给的等餐牌。你可以在未来某个时刻凭借这个牌照拿到你的食物。



只有在async函数里，才能使用await。

await后面跟的也是一个async函数。修改是等async函数返回了，才往下执行。



# async的代码和同步代码的区别是什么

## **你一定要先理解以下重点内容：**

你要把 JS 里执行分为两种。

**第一种是实打实必须由 JS 线程执行的**，比如做一些去算一个文件的 MD5 值，这种一般没人写异步，没好处，都是同步计算。

**第二种不是由 JS 线程去执行，只是 JS 把任务提交给它**，然后傻了吧唧的啥也不干等它完成并返回结果给自己。比如你调用浏览器接口去网络上下载图片，此时你的 JS 线程是把任务提交给了浏览器，然后一直等浏览器把结果返回给你。**干活的是浏览器不是你 JS 线程。**

对于不干活的情况，就得用异步的写法了，不然轻则执行效率低下，重则页面卡死，毕竟页面上那么多事等着 JS 线程去干，特别是现在的网站内容都是靠 JS 动态加载的。



以前使用的方法是回调，就是调用接口时同时传一个函数，告诉浏览器或谁执行完任务时调用函数，然后我们在函数中放一些需要执行完任务才能处理的事情。

比如让浏览器去下图片，我们就把显示图片放到函数中，这个函数就被称为回调函数。你们常见的什么 `onload` 、`onready` 都是这个意思。



但假如，我要下个文件，他的下载链接保存在 A文件里， A文件的下载链接保存在 B文件里， B文件的下载链接保存在 C文件里。

那我必须先下C文件，等C下完了拿到B的链接下B文件，再等B下完了去下A文件，最后才能在A文件里拿到我的文件下载链接。（没有这么蠢的场景，但多个任务依次依赖前一个任务完成才能处理的情况还是很常见的）



这样就会形成多层嵌套的回调，就被称为回调地狱。



于是乎，async + await 就出现了，它可以让我们用**看起来像同步的方式**去写异步的程序。



简单来说，就是async函数内部会阻塞等await，而外部调用async函数的地方不会阻塞，这就是最关键的区别。



https://www.zhihu.com/question/62254462

# 参考资料

1、理解 JavaScript 的 async/await

https://segmentfault.com/a/1190000007535316

2、async 函数的含义和用法

http://www.ruanyifeng.com/blog/2015/05/async.html

3、JS魔法堂：深究JS异步编程模型

https://www.cnblogs.com/fsjohnhuang/p/6109701.html