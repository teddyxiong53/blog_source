---
title: Linux驱动之devres框架
date: 2018-04-07 12:30:20
tags:
	- Linux驱动

---



在驱动代码里，我们经常可以看到devm开头的函数。

这些函数都是和设备资源管理相关的。

主要用来方便资源的分配。

以前没有这些devm函数的时候，在驱动probe函数里，分配资源的时候，如果失败，一般是goto到一个标签，进行资源的释放。

这样让代码看起来非常不简洁。

所以增加devm开头的函数，这种不需要你去释放，系统会帮你释放的。

相关的代码都是叫*devres.c。

所有的都在这里了。

```
teddy@teddy-ubuntu:~/work/linux-rpi/linux-rpi-4.4.y$ find -name "*devres.c"
./kernel/irq/devres.c
./sound/soc/soc-devres.c
./lib/devres.c
./drivers/gpio/devres.c
./drivers/clk/clk-devres.c
./drivers/regulator/devres.c
./drivers/base/devres.c
```

# devm框架运行的原理

前面我们说，devm框架会自动帮我们释放资源，那么是怎么做到的呢？

我们以drivers/base/devres.c为例，进行分析。



关键就在于

```
struct devres_node {
	struct list_head		entry;
	dr_release_t			release; //这个release函数是关键。失败的时候会自动调用。
#ifdef CONFIG_DEBUG_DEVRES
	const char			*name;
	size_t				size;
#endif
};
```



# 参考资料

1、linux中以devm开头的一些函数（设备资源管理）

https://blog.csdn.net/cc289123557/article/details/52137803