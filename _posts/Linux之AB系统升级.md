---
title: Linux之AB系统升级
date: 2020-03-17 11:11:11
tags:
	- Linux
---

--

Linux AB系统，也就是准备两份独立的系统固件，分别存放在flash上，系统可以选择从其中一个slot启动。

如果当前slot启动失败，可以从另外一个slot启动。

AB系统带来的一个好处，就是在开机时静默升级，用户无明显感知，下次开机自动进入升级后的系统。

还可以有效放置设备变砖，升级失败的时候，仍然可以使用之前的系统。

缺点是会增加flash的使用。

下面以rk3308的芯片上的方案为例进行分析。

rk3308的AB系统的flash布局如下：

```
|miniloader | uboot | trust | misc | boot_a | boot_b | system_a | system_b | userdata| 
```

虽然有这么多的分区，但是只有boot分区和system分区需要双分区。

但是没有提到oem分区。oem分区按道理也要双份才有意义。oem可以归类到system下。



AB系统的引导，需要一些数据来描述，方便uboot在启动时进行选择。

这个数据存放在misc分区偏移2K的位置。

有2个数据结构：

```
AvbABSlotData
AvbABData
```

CONFIG_AVB_LIBAVB_AB

uboot里有这个宏。看看哪些地方使用到了。



没有看到uboot里有使用这些代码。

跟uboot没有关系？

在这里定义的。

```
./external/avb/libavb_ab/avb_ab_flow.h:70:  uint8_t tries_remaining;
```

所以需要先把升级过程搞清楚。

怎么触发升级？

谁来负责写入升级包？写入升级的slot信息？



引导流程

```
1、开机。
2、uboot读取misc分区。
3、crc校验。
4、比较A和B的优先级。
5、如果A高，启动A。
6、在应用里，使用bootcontrol这个工具设置misc。
```



升级的代码是external/update_engine。

```

```



有了AB系统，就不需要recovery分区了。





# 编译配置

总的来说，这个主要跟uboot和应用有关系。

跟kernel没有关系。

主要是uboot里需要决定从哪个slot启动。

应用主要是来控制升级，下载镜像，写入到合适的slot里。



## uboot

需要增加这些配置：

```
CONFIG_AVB_LIBAVB=y
	这个C代码里没有用。
CONFIG_AVB_LIBAVB_AB=y
	这个C代码里没有用。
CONFIG_AVB_LIBAVB_ATX=y
    这个C代码里没有用
CONFIG_AVB_LIBAVB_USER=y
    这个C代码里没有用
CONFIG_RK_AVB_LIBAVB_USER=y
	只有这个C代码里用到了。
	
```

这个avb是什么意思？

android avb(Android Verified Boot)

这个是谷歌开源的东西，是标准的。





```
#define ANDROID_ARG_SLOT_SUFFIX "androidboot.slot_suffix="
```

从cmdline里看，当前已经生效了。

```
storagemedia=nand root=PARTUUID=cc0c0000-0000-490e-8000-1ca4000024d5 skip_initramfs androidboot.slot_suffix=_a androidboot.serialno=c3d9b8674f4b94f6  rootwait earlycon=uart8250,mmio32,0xff0c0000 swiotlb=1 console=ttyFIQ0 rootfstype=squashfs snd_aloop.index=7 snd_aloop.use_raw_jiffies=1
```

调用关系：

```
do_boot_android
	android_bootloader_boot_flow
		android_assemble_cmdline

```

目前是走这个分支的：

```
#ifdef CONFIG_ANDROID_BOOT_IMAGE
	case IMAGE_FORMAT_ANDROID:
		printf("## Booting Android Image at 0x%08lx ...\n", img_addr);
		if (android_image_get_kernel(buf, images->verify,
					     os_data, os_len))
			return NULL;
		break;
#endif
```

现在分析一下当前的uboot的各种参数配置。



```
Using default environment
Load FDT from boot_a part
DTB: rk-kernel.dtb
boot mode: normal
```

```
./arch/arm/mach-rockchip/resource_img.c:302:    printf("Load FDT from %s part\n", boot_partname);
```



# 验证

目前觉得镜像烧录和uboot引导启动没有问题。

看看升级测试。

还是update_ota.img文件。

触发命令，肯定不是recoverySystem那个了。

有这么几个工具。

## rkboot_control

这个的作用是对misc分区进行读写。

### rkboot_control

不带参数。

这个就是打印当前的misc的情况。

当前的情况：

```
magic = 
version_major = 1.
version_min = 0.
info.slot[0]->priority = 15.
info.slot[0]->tries_remaining = 0.
info.slot[0]->successful_boot = 1.
info.slot[1]->priority = 14.
info.slot[1]->tries_remaining = 7.
info.slot[1]->successful_boot = 0.
last_boot = 0.
my crc32 = dc9dd815.
crc32 = 15d89ddc
sizeof(struct AvbABData) = 32
```

### rkboot_control other

这个是把另外一个分区激活。

我们重启看看是不是从slot b启动了。

从这个uboot打印看，是从slot b启动了。

```
Load FDT from boot_b part
```

当前的misc的情况：

```
magic = 
version_major = 1.
version_min = 0.
info.slot[0]->priority = 14.
info.slot[0]->tries_remaining = 0.
info.slot[0]->successful_boot = 1.
info.slot[1]->priority = 15.
info.slot[1]->tries_remaining = 0.
info.slot[1]->successful_boot = 1.
last_boot = 1.
my crc32 = 8a39d0c1.
crc32 = c1d0398a
sizeof(struct AvbABData) = 32
```





可以看到slotb的successful_boot变成了1，就是加了一次。

所以这个机制工作正常。

现在把升级包放到板端，手动命令执行升级看看。

update_engine命令不能直接用。因为这个需要用curl来下载。

我注释掉下载的那一行代码。

手动把update_ota.img放到/tmp/update.img。

然后执行命令：

```
./update_engine update ./update_ota.img 
```

可以看到执行了升级操作。



对misc分区进行数据写入，是靠这个来做的。

````
"/dev/block/by-name/misc"
````

# bootloader_message

Android从7.0开始引入新的OTA升级方式，`A/B System Updates`，这里将其叫做`A/B`系统，涉及的内容较多，分多篇对`A/B`系统的各个方面进行分析。



# 参考资料

1、android avb（Android Verified Boot）验证

https://blog.csdn.net/weixin_43836778/article/details/90400147

2、

https://blog.csdn.net/guyongqiangx/article/details/72480154