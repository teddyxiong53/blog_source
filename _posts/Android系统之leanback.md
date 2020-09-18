---
title: Android系统之leanback
date: 2020-09-14 16:24:32
tags:
	- Android系统

---

1

看树莓派的aosp代码。

tv_core_hardware.xml里有这样的配置。

```
<feature name="android.software.backup" />
<feature name="android.software.leanback" />
<feature name="android.software.leanback_only" />
<feature name="android.software.live_tv" />
```

leanback 是什么呢？

是谷歌推出的，为了便于厂家开发TV设备的库。

对于某些使用场景，使用 Leanback 能提高开发效率，开发出来的界面也符合 Material Design 规范。

依赖 Leanback 需指定 `minSdkVersion >= 17` ，并且 Leanback 库在 `Sdk >= 21` 系统中，有**比较好的动画和阴影**等效果。

在rpi.mk也有：

```
PRODUCT_PACKAGES += \
    Launcher2 \
    LeanbackLauncher \
```



aosp-rpi3\frameworks\support\v17\leanback



参考资料

1、AndroidTV 开发之 Leanback 库简介

https://www.jianshu.com/p/d575e0c7bd59