---
title: rt-thread（二）SD卡相关
date: 2018-01-24 13:19:50
tags:
	- rt-thread

---



继续看vexpress-a9在qemu下的仿真rt-thread。

现在沿着SD卡相关的内容进行串联。

# /dev/sd0怎样注册到系统里的

1、rt_mmcsd_core_init这个是初始化的一部分。

做了这些事情：

```
1、创建一个邮箱，检测SD卡状态。
2、另一个邮箱，热拔插。
3、创建检测线程。mmcsd_detect
```

mmcsd_detect的处理：

```
while 1：
	1、检测mmcsd_detect_mb邮箱。
	2、可能情况：
		插入：
			init_mmc
				rt_mmcsd_blk_probe
					rt_device_register：就是这里注册的了
		拔出：
```

