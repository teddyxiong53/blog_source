---
title: js之async和await
date: 2019-04-22 16:03:25
tags:
	- js

---



async和await被称为是异步编程的终极解决方案。

内部实现都是用Promise实现的。

async用于声明一个函数为异步函数。

await则是等待一个异步函数执行完成。

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

如果一个async修饰的函数没有返回值，那么得到的是什么？

是Promise.resolve(undefined)。



await在等什么？

在等一个sync函数完成。

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

如果await后面的不是一个Promise，那么await表达式的运算结果就是它等到的东西。

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





参考资料

1、理解 JavaScript 的 async/await

https://segmentfault.com/a/1190000007535316