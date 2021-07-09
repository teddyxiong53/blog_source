---
title: qt之界面缩放
date: 2021-07-08 19:27:33
tags:
	- qt

---

--

我在一块720x720的lcd上运行qt的官方例子。

从显示结果看，都比较好地适应了屏幕的尺寸。怎么做到的呢？

以analogclock这个为例。

可以看到有这样的语句：

```
int side = qMin(width(), height());
painter.translate(width() / 2, height() / 2);
painter.scale(side / 200.0, side / 200.0);
```

那就是因为获取了宽高数据来决定元素的大小。

那么问题来了，为什么在基于directfb的时候，大小就不能正常适应屏幕了？

是因为尺寸数据给的不对？



再看wearable这个例子。

这个基本是用qml写的。

尺寸是320x320的。在720x720的lcd上也是满屏显示的。



参考资料

1、QML自适应屏幕分辨率的解决方案

http://www.qtcn.org/bbs/apps.php?q=diary&a=detail&did=2893&uid=92003

2、

http://www.cxyzjd.com/searchArticle?qc=qml%E7%9A%84%E5%A4%9A%E5%B1%8F%E5%B9%95%E8%87%AA%E9%80%82%E5%BA%94&page=1