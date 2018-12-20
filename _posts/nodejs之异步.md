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

但是如果

参考资料

1、node.js异步控制流程 回调，事件，promise和async/await

https://www.cnblogs.com/kazetotori/p/6043983.html