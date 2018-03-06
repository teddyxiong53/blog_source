---
title: rt-thread（二）SD卡相关
date: 2018-01-24 13:19:50
tags:
	- rt-thread

---



继续看vexpress-a9在qemu下的仿真rt-thread。

现在沿着SD卡相关的内容进行串联。



# 代码分布

代码主要分布在2个地方：

1、bsp/qemu-vexpress-a9/drivers下的drv_sdio.c和drv_sdio.h。

```
drv_sdio.h内容：
struct sdhci_t
struct sdhci_cmd_t
struct sdhci_data_t
```



2、components/drivers/sdio目录下。

```
sd.c
sdio.c
mmc.c
mmcsd_core.c
blk_dev.c
```

# vexpress板子的sdio寄存器分布

1、基地址在0x10005000



# /dev/sd0怎样注册到系统里的

1、rt_mmcsd_core_init这个是初始化的一部分。

做了这些事情：

```
1、创建一个邮箱，检测SD卡状态。
2、另一个邮箱，检测热拔插。
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

检测邮箱的消息来源：

bsp/qemu/drivers目录下的drv_sdio.c里。

```
pl180_init
	1、mmcsd_alloc_host分配得到一个rt_mmcsd_host结构体。
	2、芯片相关的sdhci_t结构体初始化，并且给到rt_mmcsd_host里的private_data。
	3、mmcsd_change。这里就是发送了邮箱。触发检测线程的动作。
```



结构体rt_mmcsd_host是整个SD卡相关驱动的核心结构体。

```
1、card结构体。
2、rt_mmcsd_host_op结构体。
3、private_data指向芯片相关的内容。
4、io_cfg结构体。
```



5个头文件

mmc.h：主要是红定义。另外声明个接口：mmc_send_op_cond、init_mmc。

mmcsd_card.h

```
1、定义SD卡内部寄存器的结构体，方便解析和使用。
2、主结构体rt_mmcsd_card。
```

mmcsd_cmd.h

```
1、定义class0到class11的命令的宏。
```

mmcsd_core.h

```
1、定rt_mmcsd_data/cmd/req结构体。
2、一堆的mmcsd_xx函数。
```

mmcsd_host.h

```
1、定义rt_mmcsd_host结构体。
```

