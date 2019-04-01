---
title: Android之多用户
date: 2019-04-01 13:25:32
tags:
	- Android
---



一个app被安装后，系统给APP分派了一个唯一的“Application ID”。简称“AppId”。

同时系统里有多个用户，每个用户有一个UserId。

Android里的UserId跟Linux下的uid不是一个东西。

转化公式是：

```
uid = UserId *10000 + AppId
```

usb连上书籍，搜索微信相关进程。

```
osborn:/ $ ps |grep tencent.mm
u0_a146   8995  736   3054208 204232          0 0000000000 S com.tencent.mm
u0_a146   9921  736   2412628 36824          0 0000000000 S com.tencent.mm:push
u0_a146   17716 736   2400420 32108          0 0000000000 S com.tencent.mm:sandbox
u0_a146   30610 736   2398872 26428          0 0000000000 S com.tencent.mm:exdevice
```

u0_a146就是UserId。

第二列是pid。

第三列是ppid。

u0_a146这个怎么计算呢？

以下划线作为分界线。

前面的u0是UserId。后面的a146是AppId。

计算是这样：

```
u0_a164 = 0 * 10000 + (10110) = 10110
a110里的a翻译为10000。表示一万。
这个是代码里写死的公式。
```



从Android5.0开始，引入了多用户api。

引入多用户的目的是什么？

```
1、实现访客模式。
2、应用多开。
```



参考资料

1、Android 多用户 —— 从入门到应用分身 (上)

https://www.itcodemonkey.com/article/6169.html

