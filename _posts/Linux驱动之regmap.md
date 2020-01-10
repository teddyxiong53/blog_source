---
title: Linux驱动之regmap
date: 2020-01-07 17:31:08
tags:
	- Linux

---

1

什么是regmap？主要用来做什么？

regmap是内核3.1版本引入的一套控制总线通用接口。

什么是控制总线？i2c和spi就是控制总线。

在没有regmap之前，当设备驱动使用i2c或者spi的时候，都需要写一堆的boardinfo。然后注册到系统。

光是注册就很麻烦了，更何况还存在i2c和spi的读写接口不一致的情况。

regmap就是为了改善这种情况，提供了一层抽象。

有了regmap，不管底层是i2c还是spi，读写接口都是一样的。

还可以在驱动和硬件ic之间做一层缓存，减少跟外部芯片操作的次数。



架构层次

分为3层

```
regmap   |  regmap_read 和regmap_write
-----------------------------------
regcache | flat   lzo  rbtree
-----------------------------------
bus      |    i2c spi   mmio  ac97
```

有3个核心结构体：

```
regmap_config
regmap_ops
regmap_bus
```



参考资料

1、设备驱动中的regmap

https://blog.csdn.net/viewsky11/article/details/54295679

2、regmap简介

https://blog.csdn.net/lk07828/article/details/50587879