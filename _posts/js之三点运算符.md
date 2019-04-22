---
title: js之三点运算符
date: 2019-04-22 17:21:25
tags:
	- js

---



三个点是ES6新增的语法。叫做扩展运算符。

作用是把数组转化为都好分隔的参数。

```
console.log(...[1,2,3]);
```

主要是用于函数调用。

```
function add(a, b) {
	return a+b;
}
var numbers = [1,2];
var result = add(...numbers);
console.log(result);
```



```
const commonParam = {
    key: 'xx',
    location: 'beijing',
    lang: 'zh-cn',
    unit: 'm'
}
function test(...a) {
	console.log(a);
}
test(commonParam);
```

结果：

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ node app.js 
[ { key: 'xx', location: 'beijing', lang: 'zh-cn', unit: 'm' } ]
```



参考资料

1、es6 扩展运算符 三个点（...）

https://blog.csdn.net/qq_30100043/article/details/53391308