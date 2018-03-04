---
title: 树莓派移植uboot
date: 2016-11-12 17:20:20
tags:
	- 树莓派
---



##1.下载最新版本的uboot代码



##2.配置uboot

树莓派3b有2个配置文件：rpi_3_32b_defconfig 和rpi_3_defconfig。

这2个文件内容就一行有区别：

```
CONFIG_ARM=y
CONFIG_ARCH_BCM283X=y
CONFIG_TARGET_RPI_3_32B=y  #这一行不同CONFIG_TARGET_RPI_3=y 
CONFIG_SYS_MALLOC_F_LEN=0x2000
CONFIG_DEFAULT_DEVICE_TREE="bcm2837-rpi-3-b" 
CONFIG_DISTRO_DEFAULTS=y
CONFIG_OF_BOARD_SETUP=y
# CONFIG_DISPLAY_CPUINFO is not set
# CONFIG_DISPLAY_BOARDINFO is not set
CONFIG_SYS_PROMPT="U-Boot> "
# CONFIG_CMD_FLASH is not set
# CONFIG_CMD_FPGA is not set
CONFIG_CMD_GPIO=y
CONFIG_CMD_MMC=y
CONFIG_CMD_USB=y
CONFIG_OF_EMBED=y
CONFIG_ENV_FAT_INTERFACE="mmc"
CONFIG_ENV_FAT_DEVICE_AND_PART="0:1"
CONFIG_DM_KEYBOARD=y
CONFIG_DM_MMC=y
CONFIG_MMC_SDHCI=y
CONFIG_MMC_SDHCI_BCM2835=y
CONFIG_DM_ETH=y
# CONFIG_REQUIRE_SERIAL_CONSOLE is not set
CONFIG_USB=y
CONFIG_DM_USB=y
CONFIG_USB_DWC2=y
CONFIG_USB_STORAGE=y
CONFIG_USB_KEYBOARD=y
CONFIG_USB_HOST_ETHER=y
CONFIG_USB_ETHER_SMSC95XX=y
CONFIG_DM_VIDEO=y
CONFIG_SYS_WHITE_ON_BLACK=y
CONFIG_CONSOLE_SCROLL_LINES=10
CONFIG_PHYS_TO_BUS=y
CONFIG_OF_LIBFDT_OVERLAY=y
```

在代码里的就一点不同。

```
#if defined(CONFIG_TARGET_RPI_2) || defined(CONFIG_TARGET_RPI_3_32B)
#define CONFIG_SKIP_LOWLEVEL_INIT
#endif
```

我们选择rpi_3_32b_defconfig 这种。

设备树文件是arch/arm/dts/bcm2837-rpi-3-b.dts

我们分析一下。

```
bcm2837-rpi-3-b.dts
	bcm2837.dtsi
		bcm283x.dtsi这个里面内容最多。
		
	bcm2835-rpi.dtsi
		定义了内存的范围。gpio、i2c等。
	bcm283x-rpi-smsc9514.dtsi
		
	bcm283x-rpi-usb-host.dtsi
	自己也定义了memory的范围，就覆盖了上面bcm2835-rpi.dtsi里定义的。
	
```

## 3. 编译

make就好了。

## 4. 配置uboot环境变量

因为是使用U盘引导，所以首先要使能usb，同时扫描usb设备并读取image和dtb文件。修改uboot环境变量如下：

```
setenv bootcmd "usb start; fatload usb 0:1 ${fat_addr_r} /bcm2708-rpi-b.dtb; fatload usb 0:1 {loadaddr} /uImage; bootm {loadaddr} -${fdt_addr_r}";
setenv bootargs "console=/dev/ttyAMA0,115200 rootdev=/dev/sda2 rootfstype=ext4 rootwait";
sa
```

如果是SD卡的话，这样配置：

```
mmc rescan
fatload mmc 0:1 ${loadaddr} imagefile
bootm
```



# 5. 编译支持设备树的内核

```
make uImage 
make dtbs
cp arch/arm/boot/dts/bcmd2708-rpi-b.dtb release
```

拷贝到U盘的boot分区。

启动过程的打印：

```
## Flattened Device Tree blob at 00000100
   Booting using the fdt blob at0x000100
   Loading Kernel Image ... OK
   Loading Device Tree to07b42000, end 07b477e3 ... OK
```

