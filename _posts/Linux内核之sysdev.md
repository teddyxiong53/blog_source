---
title: Linux内核之sysdev
date: 2019-12-05 11:22:28
tags:
	- Linux
---

1

看bsp代码，看到sysdev的注册。

了解一下这个。

简单百度了一下，没有找到相关文章。

看代码里的注释。

sysdev是System device。

是一种略有不同的设备模型。

它们不需要动态跟driver绑定，也不能被probe。

也不跟任何总线关联。

所以我们对它进行特殊处理。

我们对sysdev还是有一个driver的概念的。

因为我们还是想要对这些sysdev进行基本操作。

我们也想对某些类型的进行动态driver绑定。

典型的设备是硬件定时器。看门狗。

注册：

```
static __init int s3c24xx_clk_driver(void)
{
	return sysdev_driver_register(&s3c2440_sysclass, &s3c2440_clk_driver);
}
```



参考资料

1、

