---
title: js之各种for循环
date: 2019-04-30 11:23:25
tags:
	- js

---



js的for循环这些年来在不断变化。有这些for循环的形式。

#基本for

最原始的方式：

```
var arr = ["a", "b", "c"];
for(var i=0; i<arr.length; i++) {
    console.log(arr[i])
}
```

#forEach方法

ES5加入了forEach方法。这个方法是Array.prototype里的。所以只有数组类型才能用。

这种方法的缺点是：你不能break出来。

```
var arr = ["a", "b", "c"];
arr.forEach(function(value) {
    console.log(value);
})
```

#for-in

另外，还有for in循环。

```
var arr = ["a", "b", "c"];
for(var index in arr) {
    console.log(arr[index]);
}
```

for-in本来是设计给遍历对象用的。

用来遍历数组，可能隐藏不少问题。

```
var obj = {
    name: "xx",
    age: 10,
    height: 170
}
for(var key in obj) {
    console.log(key+ ": " + obj[key])
}
```

# for-of

这个是ES6引入的。

上面说了。用for-in来遍历数组，可能有问题。

所以就专门推出了for-of来专门用来高效率地遍历数组。

```
var arr = ["a", "b", "c"]
for(var element of arr) {
    console.log(element);
}
```

for-of不能用来遍历对象的属性。







参考资料

1、深入浅出 ES6（二）：迭代器和 for-of 循环

https://www.infoq.cn/article/es6-in-depth-iterators-and-the-for-of-loop

