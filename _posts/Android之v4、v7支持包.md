---
title: Android之v4、v7支持包
date: 2019-03-30 11:28:32
tags:
	- Android
typora-root-url: ../
---





什么是支持包？为什么需要支持包？当前有哪些支持包？



支持包是Android sdk之外的一些零散的jar包。

谷歌也希望都可以放在Android sdk里，但是做不到呀。

Android发展快，变化大。

支持包的的原因：

1、向后兼容。

```
例如，我们的app，需要支持的minSdkVersion是9（对应2.3版本），targetSdkVersion是11（对应3.0）。
然后我们在代码里使用了ActionBar。
但是这个组件在2.3版本里是没有的。我们的app安装在2.3版本的Android上，运行是会崩溃的。
那怎么办？
谷歌提供的解决方案是这样的：
每次发布新的sdk时，把新增的接口，提取出来放在支持包里，开发者在碰到上面这样的问题时，就把支持包打包进app。
这样就不会崩溃了。
```

2、提供不适合打包进framework的功能。

```
谷歌对app官方提供了推荐设计。
目的是希望Android应用有比较统一的交互设计，这样就可以降低用户的使用成本。
但是这个仅仅是推荐奖，不强制要求开发者如此做。
所以以jar包的方式提供。例如DrawerLayout等都是这种情况。
```

3、支持不同形态的设备。



谷歌一共提供了13类支持包。一般我们常用的是v4和v7这2个集合包。



v4介绍

```
1、最低支持是从2.3版本开始。就是api level 9。
2、这个支持包也有版本号的。
	例如这样：android-suppport-v4-23.0.0，对应api level 23 。
	一般碰到引入了v4包，但是还是找不到方法，一般就是引入的v4包的版本不对。
	
```

v4包的主要api

```
compat 
	兼容一下framework api。例如Context.getDrawable()
	
core-utils
	提供一下核心工具类。
core-ui
media-compat
fragment

```

![](/images/android-v4-support.webp)





参考资料

1、Android Support Library 的前世今生

https://juejin.im/entry/57e8d525bf22ec00587a5848

2、android support v4支持包要点分析，api介绍

https://www.jianshu.com/p/d36a1e5bf246

3、支持库

https://developer.android.com/topic/libraries/support-library