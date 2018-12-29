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



参考资料

1、

