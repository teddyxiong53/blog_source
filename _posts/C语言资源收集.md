---
title: C语言资源收集
date: 2019-04-10 15:11:31
tags:
	- C语言

---





通用C基础库

https://github.com/gozfree/gear-lib

```
从git版本记录里，看看。
1、首先加进来的是liblog。这个还不错，有不同的颜色。可以集成到自己的项目。
2、libgevent。开始的版本只支持epoll。
	这个编译有点问题。稍微改一下就好了。
	相当于对select、epoll的一个简单封装。
3、libdict。这个值得学习以。
4、libsort。排序算法库。
	实现了heapsort和bubble sort。
5、libworkq。
	不知道用户态的workqueue有什么用。
6、libskt。
	编译不过。是socket库。
7、librbtree。
	这个是从kernel里扒出来的。
	
libconfig
	这个把ini和json这些综合起来了。
librtsp
	这个有价值。
```

