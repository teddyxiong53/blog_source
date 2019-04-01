---
title: Android之Activity启动过程
date: 2019-04-01 15:13:32
tags:
	- Android
---



在Android系统里，Activity和Service是app的核心组件，它们以松散的方式耦合在一起，构成了一个完整的app。

这个得益于framework提供了一套完整的机制来协助app启动这些Activity和Service。

framework提供了Binder来帮助它们进行通信。



有两种情况会导致Activity的启动。

1、用户点击app图标。

2、在一个应用里用startActivity启动。



我们看看startActivity的情况。

我们只需要这样：

````
Intent intent = new Intent("com.xhl.SecondActiviy");
startActivity(intent);
````

FirstActivity跟SecondActivity耦合非常松散，就是一个字符串来传递。

这个得益于framework的强大。

当然还需要在manifest里配置一下。

```

```



参考资料

1、Android应用程序的Activity启动过程简要介绍和学习计划

https://blog.csdn.net/luoshengyang/article/details/6685853