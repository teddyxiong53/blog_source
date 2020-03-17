---
title: Linux之AndroidImage
date: 2020-03-17 14:11:11
tags:
	- Linux
---

1

看rockchip的uboot里，是使用了Android的image格式。

Android的image格式有什么不一样的？

CONFIG_ANDROID_BOOT_IMAGE 这个是宏开关。

cmd/bootm.c

common/image.c

resource_img.c

主要是这3个文件里用到了。

image格式主要有这4个宏：

```
0：invalid
1：legacy
2：基于设备树的
3：Android boot image
```

现在bootm分为这些阶段了：

```
1：start
2：find os
4：find other
8：load os
10： ramdisk
20： fdt
40： os cmdline
80： os bd t
100： osprep
200： os fake go
400： os go
```



当前的bootcmd是这样：

```
bootcmd=boot_android ${devtype} ${devnum};bootrkp;run distro_bootcmd;
```

bootargs是这样：

```
bootargs=storagemedia=nand
```

展开后的bootcmd是这样：

```
bootcmd = boot_android nand 0 ; bootrkp; run distro_bootcmd
```

可以看到是分成了3个阶段。

第一阶段：

```
boot_android nand 0
```

```
do_boot_android
	完整的参数是这样：
	<interface> <dev[:part|;part_name]> <slot> [<kernel_addr>]
	至少是要3个参数的：
	nand 0 a 
	然后调用了android_bootloader_boot_flow
		1、拿到misc分区。
		2、load and clear 启动mode
			mode有三种：normal、recovery、bootloader。
		android_image_load
		android_assemble_cmdline
		android_bootloader_boot_kernel
			do_bootm
				do_bootm_states
					这里把bootm的那些flags都或上了。
					所以会顺序执行：
						bootm_start
						bootm_find_os
						bootm_load_os
						bootm_os_get_boot_func
						boot_selected_os
							这里就一去不复返了。
```

第二阶段：bootrkp

```
bootrkp
	do_boot_rockchip
		boot_rockchip_image
```

第三阶段：run distro_bootcmd

```
"distro_bootcmd=" BOOTENV_SET_SCSI_NEED_INIT                      \
		"for target in ${boot_targets}; do "                      \
			"run bootcmd_${target}; "                         \
		"done\0"
```

```
boot_targets=mmc1 mmc0 rknand0 pxe dhcp 
```

我们当前的情况是rknand0这个。

展开的值是：

```
bootcmd_rknand0=setenv devnum 0; run rknand_boot
```

rknand_boot

```
rknand_boot=if rknand dev ${devnum}; then setenv devtype rknand; run scan_dev_for_boot_part; fi
```

scan_dev_for_boot_part

```
这个就不进一步展开了。
```



参考资料

