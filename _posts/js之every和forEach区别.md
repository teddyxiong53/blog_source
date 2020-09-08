---
title: js之every和forEach区别
date: 2020-09-08 16:53:17
tags:
	- js

---

1

这些都是应用在Array上的。

迭代器方法， 这些方法对数组中的每一个元素应用一个函数，可以返回一个值，一组值或一个新数组

# forEach

不生成新数组的迭代器方法

```javascript
function square(num) {
    console.log(num, num*num)
}
var nums = [1,2,3]
nums.forEach(square)
```



# every

这个方法，接受一个返回值为布尔值的函数。

对数组里的每个元素应用这个函数。

如果对于所有元素，函数返回值都是true，则返回true。否则返回false。

```javascript
function isEven(num) {
return num%2 === 0
}
var nums = [1,2,3]
var even = nums.every(isEven)
if(even) {
console.log("all num are even")
} else {
console.log("not all nums are even")
}
```

# reduce

这个是特点是对每个元素进行累加。

元素可以是数组，也可以是字符串。



参考资料

1、JS数组方法（forEach()、every()、reduce()）

https://www.cnblogs.com/MandyCheng/p/8047771.html