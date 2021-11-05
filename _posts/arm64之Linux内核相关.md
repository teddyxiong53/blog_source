---
title: arm64之Linux内核相关
date: 2020-08-31 14:01:59
tags:
	- arm
---

1

我们都知道，一个系统的启动的基本流程是先bootloader然后运行kernel。

**当对所有CPU上电后，那么所有的CPU都会从bootrom里面开始执行代码**，

为了防止并发的一些问题，**有必要将除了primary cpu以外的cpu拦截下来**。

使boot的过程是顺序的，而不是并发的。

在 启动的过程中，bootloader中有一道栅栏，它拦住了除了cpu0外的其他cpu。

cpu0直接往下运行，进行设备初始化以及运行Linux Kernel。

**其他cpu则在栅栏外进入睡眠状态。**

cpu0在初始化smp的时候，会在cpu-release-addr里面填入一个地址并唤醒其他 cpu。

这时候，在睡眠的这个cpu接受到了信号，

醒来的时候先检查下cpu-release-addr这个地址里面的数据是不是不等于0。

如果不等于 0，意味着主cpu填入了地址，该它上场了。它就会直接填入该地址执行。

是不是发现了上面所介绍的方法非常简单？

是的。简直简单的不像是社区这些高智商的人写的。

所以，一份更难的版本出来了。

现在社区已经抛弃上面的方法，转而投向另外一种enable-method。那就是psci。

在设备树里有这样的：

```
cpu {
	enable-method = "psci";
}
psci {
		compatible = "arm,psci-1.0";
		method = "smc";
	};
```



参考资料

1、

https://blog.csdn.net/eric43/article/details/81154430