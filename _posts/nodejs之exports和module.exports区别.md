---
title: nodejs之exports和module.exports区别
date: 2019-04-16 14:00:28
tags:
	 - nodejs
---



```
1、module.exports初始值为一个空对象{}
2、exports是指向module.exports的引用。
3、require()函数返回的是module.exports。
```

我们经常看到这种写法：

```
exports = module.exports = xxx;
```



每一个nodejs文件，都自动创建了一个module对象。

同时，module对象会创建一个叫exports的属性。初始化值为{}





参考资料

1、exports 和 module.exports 的区别

https://cnodejs.org/topic/5231a630101e574521e45ef8

2、module.exports与exports？？关于exports的总结

https://cnodejs.org/topic/52308842101e574521c16e06