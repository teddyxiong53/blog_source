---
title: cpp之new后面带括号和不带括号区别
date: 2019-03-20 10:21:32
tags:
	- cpp

---



1

这个要分两种情况来讨论。

一个是基础类型，一个是自定义类型。

基础类型：

```
int *a = new int;//这个指针a的值是随机的。
int *b = new int();//这个b指针的值会被设置为0 。
```

结论：就是一定要使用括号。



对于定义的class。有分几种情况讨论。

但是不重要，带括号使用就好了。



参考资料

1、new 对象加括号和不加括号的区别

https://blog.csdn.net/eldn__/article/details/41963727