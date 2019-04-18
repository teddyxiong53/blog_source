---
title: 小程序之page之间通信
date: 2019-04-18 14:34:25
tags:
	- 小程序

---



一个常见的双tab框架：

```
A     B
   |
   V
   C
   |
   V
   D
```

总共4个page。

我们假设这样一种场景：

pageA有一个数，当我们从A起到C，做了一些操作，C修改了这个数字。再回到A的时候，这个数字需要刷新。

A和B是兄弟页面。

A和C是父子页面。



```
wx.getStorageSync("codeNumber");
wx.setStorageSync("codeNumber");

```



参考资料

1、微信小程序页面间通信的5种方式

http://www.wxapp-union.com/portal.php?mod=view&aid=1830

这个文章是完整的，但是没有图片，上面一篇有图片。

https://segmentfault.com/a/1190000008895441

