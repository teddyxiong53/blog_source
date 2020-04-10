---
title: rk3308的Linux开发包分析
date: 2018-10-11 13:57:51
tags:
	- Linux

---



RK3308的开发包是基于buildroot来做的。 

从使用上来看，编译比较简单，分两步：

1、设置环境。

```
source envsetup.sh 
```

根据提示，选择要编译的版本。例如我们选择32位的release版本。rockchip_rk3308_32_release

2、编译。

```
./build.sh
```

这个脚本可以带一个参数，参数是要编译的模块的名字。

envsetup.sh的结果是，

```
make -C /home/hlxiong/work/rk3308/buildroot O=/home/hlxiong/work/rk3308/buildroot/output/rockchip_rk3308_32_release 
```

我们看看这个Makefile里怎么写的。

这个Makefile是被自动生成的，里面的修改没用。

被buildroot/support/scripts/mkmakefile生成。

我们找到rockchip_rk3308_32_release_defconfig这个配置文件。

在这里./buildroot/configs/rockchip_rk3308_32_release_defconfig。

配置项大概80条。

我们再看build.sh脚本。

如果没有参数，就是build all和save all。

```
if [ ! -n "$1" ];then
	echo "build all and save all as default"
	BUILD_TARGET=allsave
else
	BUILD_TARGET="$1"
	NEW_BOARD_CONFIG=$TOP_DIR/device/rockchip/$RK_TARGET_PRODUCT/$1
fi
```

增量编译做得很好。

配置项在device/rockchip/.BoardConfig.mk里。



文档也写得比较齐全。

buildroot下的编译。

```
source buildroot/build/envsetup.sh
```

build.sh

```
该脚本会自动配置环境变量， 编译 U-Boot， 编译 Kernel， 编译 Buildroot， 编译 Recovery
继而生成固件。
```



adb reboot bootloader

这个可以进入烧录模式。

# GPT

boot过程介绍

首先我们需要理清楚概念，在启动Linux系统的过程中，有多个启动阶段。

我们需要知道image打包的方式，image应该被放置的位置。

最后，我们需要知道怎样把image写入到不同个介质上，并且从介质上启动。

rk使用GPT作为主要的分区表。







parameter.txt怎样生成的？

```
./rk3308/mkfirmware.sh:74:      cp -a $PARAMETER $ROCKDEV/parameter.txt
```

$PARAMETER 这个就是我们手动改的参数文件。





https://github.com/rockchip-linux/rkbin

http://opensource.rock-chips.com/wiki_Partitions

http://opensource.rock-chips.com/wiki_Boot_option

# trust分区

**trusted-os like ATF, OP-TEE**



# repo管理

代码使用了repo来进行版本管理。



# 镜像生成过程

## 编译u-boot过程

通过一个make.sh脚本来调用编译的。

脚本的用法：

```
./make.sh [board|subcmd] [O=<dir>]
    - board: board name of defconfig"
    - subcmd: loader|loader-all|trust|uboot|elf|map|sym|<addr>|"
    - O=<dir>: assigned output directory"
默认只传递了一个defconfig名字。
```

可以做这些打包操作：

```
./make.sh trust                    --- pack trust.img"
./make.sh uboot                    --- pack uboot.img"
./make.sh loader                   --- pack loader bin"
./make.sh loader-all	           --- pack loader bin (all supported loaders)"
```



```
 load addr is 0x600000!
pack input ./u-boot.bin 
pack file size: 610923 
crc = 0x913bb5ac
uboot version: U-Boot 2017.09-gb8393f4-dirty (Apr 08 2020 - 15:01:13)
pack uboot.img success! 
pack uboot okay! Input: ./u-boot.bin
out:rk3308_loader_v1.26.111.bin
fix opt:rk3308_loader_v1.26.111.bin
merge success(rk3308_loader_v1.26.111.bin)
pack loader okay! Input: /home/hlxiong/work2/rk3308_cmcc/rkbin/RKBOOT/RK3308MINIALL.ini
/home/hlxiong/work2/rk3308_cmcc/u-boot
out:trust.img
merge success(trust.img)
/home/hlxiong/work2/rk3308_cmcc/u-boot
pack trust okay! Input: /home/hlxiong/work2/rk3308_cmcc/rkbin/RKTRUST/RK3308TRUST.ini

Platform RK3308 is build OK, with new .config(make doss_wb220b_defconfig)
```

prebuilt的工具链是用来编译uboot的。



打包了3个img：

miniloader、uboot.img、trust.img。

这些算是黑盒性质的东西，都是不开源的二进制。



## 编译kernel

这个就编译了kernel和dtb文件。

直接使用Makefile做的。没有什么特别的地方。

## 编译rootfs

这个就是编译buildroot。

buildroot里没有配置uboot和kernel。所以也就剩下rootfs了。

这里有一个配置项，就是是否把oem放进rootfs分区里。默认都是否的。

看到每次都会执行这个：make partinit-rebuild 

这个的目的是什么呢？这个是rk自己定义的一个package。

就是执行一些安装操作。

没有什么特别的。

看到后面recovery的，可以看出，这个会根据编译release和recovery，而调整参数进行partinit。所以是非常关键而且必要的。

编译是靠$COMMON_DIR/mk-buildroot.sh 这个脚本来调用的。

这个脚本也没有做什么特别的事情，就是先envsetup.sh一下，然后调用buildroot的make。

## 编译recovery

这个的特别之处在于：

```
cd $TOP_DIR/buildroot/output/$RK_CFG_RECOVERY/
oem_root_fs_type=$RK_OEM_FS_TYPE
export RK_OEM_FS_TYPE=ext2 # 修改了oem的属性为ext2的。
make partinit-dirclean && make partinit-rebuild  # 这里就可以看到partinit的作用了。
export RK_OEM_FS_TYPE=$oem_root_fs_type
cd $TOP_DIR/
```

编译镜像：

```
$COMMON_DIR/mk-ramdisk.sh recovery.img $RK_CFG_RECOVERY
```

先输出一下recovery的环境变量。

```
source $TOP_DIR/buildroot/build/envsetup.sh $RAMDISK_CFG
```

然后还是用recovery的配置来进行buildroot的编译（这个就少了很多包了）。

最后打包内容：CPIO_IMG就是rootfs的。把rootfs、kernel、dtb这3个东西打包就得到recovery.img。

```
mkbootimg --kernel $KERNEL_IMAGE --ramdisk $CPIO_IMG --second $KERNEL_DTB -o $TARGET_IMAGE
```

target目录，release的有110M左右（近4000个文件）。而recovery的只有17M（580个文件）。



# 升级包的生成

是靠tools\linux\Linux_Pack_Firmware\rockdev这个目录下的配置文件来指定打包哪些内容到升级包里。

update.img，是默认把所有内容打包进去的。

```
rk3308-package-file    全量升级包。
rk3308-package-file-ab   AB系统升级的
rk3308-package-file-ota  recovery方式升级的ota包。
rk3308-package-file-rootfs
```



# misc分区

就是一个裸的flash操作。

里面会放几个参数，主要是方便recovery和ab系统在升级时做标记。

查看misc分区的内容：

```
/dev/block/by-name # hexdump /dev/block/by-name/misc -C                       
00000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*                                                                             
00004340  66 61 6c 73 65 00 00 00  00 00 00 00 00 00 00 00  |false...........|
00004350  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*                                                                             
00100000                                                                      
/dev/block/by-name #                                                          
```



# 内存布局

内存是在靠近0的位置上的。



# uboot里的一些配置

```
(0xff000500) Rockchip boot mode flag register address
(0x0) Size of IRAM reserved in SPL 

[*] Support for Rockchip Image Bootloader boot flow 
[*]   Rockchip vendor storage partition support 
[*]   Using dtb from Kernel/resource for U-Boot 

[*] Rockchip pre-loader atags  
[*] Rockchip pre-loader serial 

```

```
[*] Enable support for Android Boot Images 
[*] Support Flattened Image Tree           
```



```
[*] Enable driver model key support 
[*] Enable gpio keys support 
```

```
--- Rockchip Flash Devices support                    
      *** Rockchip Flash Devices ***                  
[*]   Rockchip NANDC Slc Nand Devices support         
[*]   Rockchip SFC SPI Nand Devices support           
[*]   Rockchip SFC SPI Nor Devices Support            
```

# uboot如何拿到boot分区里的dtb的？

```
#define CONFIG_OF_SEPARATE 1
```

```
/* FDT is at end of image */
	gd->fdt_blob = (ulong *)&_end;
```

看起来不是从kernel里拿到的。

但是又不对啊。

我在uboot下面，根本找不到字符串“gpio-keys”。

事实上，我们又通过这个来获取按键来检测是否应该进入到烧录模式。

那就要看uboot.img里打包了什么东西。

没有看到打包dtb文件的操作。

在uboot的Makefile里，有这样的语句：

```
ifeq ($(CONFIG_USING_KERNEL_DTB),y)
u-boot-dtb.bin: u-boot-nodtb.bin dts/dt-spl.dtb FORCE
else
u-boot-dtb.bin: u-boot-nodtb.bin dts/dt.dtb FORCE
endif
```

当前这个配置是打开的。

```
./include/generated/autoconf.h:211:#define CONFIG_USING_KERNEL_DTB 1
./include/config/auto.conf:209:CONFIG_USING_KERNEL_DTB=y
```



```
rknand_blk_bind
	blk_create_devicef
		blk_create_device
			device_bind_driver
				device_bind_with_driver_data
					#ifdef CONFIG_USING_KERNEL_DTB
                        if (gd->flags & GD_FLG_RELOC) {
                            /* For mmc/nand/spiflash, just update from kernel dtb instead bind again*/
                            if (drv->id == UCLASS_MMC || drv->id == UCLASS_RKNAND ||
```

# uboot里操作gpio

这样就可以读取到按键的值了。

```
gpio_request
gpio_direction_input
gpio_get_value

```

# 怎样进入到recovery系统

这个要看rk自己的recoverySystem这个命令里是怎么做的。

我们执行recoverySystem不带参数：

有一个重要的数据结构：

```
struct bootloader_message {
    char command[32];
    char status[32];
    char recovery[768];
    char systemFlag[256]
};
```

填写内容：

```
strlcpy(msg.command, "boot-recovery", sizeof(msg.command));
    strlcpy(msg.recovery, "recovery\n--wipe_data", sizeof(msg.recovery));
    strlcat(msg.recovery, "\n", sizeof(msg.recovery));
    strlcpy(msg.systemFlag, "false", sizeof(msg.systemFlag));
```



所谓发送bootloader message，就是往misc分区里写这个结构体。

```
int set_bootloader_message(const struct bootloader_message *in)
	FILE* f = fopen(MISC_NODE, "wb");//"/dev/block/by-name/misc"
	//也不是直接写，偏移了16K。
	fseek(f, BOOTLOADER_MESSAGE_OFFSET_IN_MISC, SEEK_SET);
```

然后重启：

```
reboot(RB_AUTOBOOT);
```

如果是安装升级包：

```
void installPackage(char *update_file){
    struct bootloader_message msg;
    memset(&msg, 0, sizeof(msg));
    strlcpy(msg.command, "boot-recovery", sizeof(msg.command));
    strlcpy(msg.recovery, "recovery\n--update_package=", sizeof(msg.recovery));
    strlcat(msg.recovery, update_file, sizeof(msg.recovery));
    strlcat(msg.recovery, "\n", sizeof(msg.recovery));
    strlcpy(msg.systemFlag, "false", sizeof(msg.systemFlag));
```

boot-recovery 这个是一个命令吗？

grep这个字符串，可以找到2个工具有这个字符串。

```
匹配到二进制文件 ./usr/bin/update
匹配到二进制文件 ./usr/bin/recoverySystem
```

update这个工具也是rk提供的，在external/update_engine目录下。

不是在这里，而是在package\rockchip\update目录下，只有一个C文件，也放在这里。

编译是这样的：

```
define UPDATE_BUILD_CMDS
	$(TARGET_CC) $(TARGET_CFLAGS) $(TARGET_LDFLAGS) $(RECOVERY_BUILD_OPTS) \
		package/rockchip/update/update.c package/rockchip/update/update_recv/update_recv.c -o $(@D)/update
endef
```

是2个C文件。

看一个这个工具的逻辑：

```
不带参数或者带参数factory/reset
	都是执行rebootWipeUserData
如果参数是ota或者update
	执行rebootUpdate(0);
```

# 启动参数



执行adb reboot bootloader。

看到查看有这个打印：

```
Returning to boot ROM
```

这个是两种情况会进。

一个是在SPL方式下。一个就是下载模式。当前SPL方式是关闭的。所以只有下载模式会打印这个。

```
enum rockchip_bootrom_cmd {
	/*
	* These can not start at 0, as 0 has a special meaning
	* for setjmp().
	*/

	BROM_BOOT_NEXTSTAGE = 1,  /* continue boot-sequence */
	BROM_BOOT_ENTER_DNL,      /* have BROM enter download-mode */
};
```

靠检测0xff000500这个寄存器的值。

```
boot mode: loader
enter Rockusb!
```

现在电脑上烧录工具看到的就是进入了loader模式了。



升级包的打包过程

rk3308-package-file-rootfs 这个是处理oem在rootfs 情况的。

如果配置了AB升级。

```
if [ "$RK_LINUX_AB_ENABLE" == "true" ]; then
	    ln -fs $PACK_TOOL_DIR/rockdev/rk3308-package-file-ab $PACK_TOOL_DIR/rockdev/package-file
	fi
```

我现在是这2种情况都包括。

既把oem放到了rootfs，也把AB系统打开了。

所以最终起作用的是rk3308-package-file-ab 这个配置文件。

在这个文件里，把oem的注释掉。

update.img就是包括了所有分区的一个包。

打包操作过程：

```
./afptool -pack ./ Image/update.img || pause
./rkImageMaker -RK3308 Image/MiniLoaderAll.bin Image/update.img update.img -os_type:androidos || pause
echo "Making update.img OK."
```

打包AB系统ota包的函数，在build.sh里。

```
function build_ota_ab_updateimg()
```

包名没有做区分，统一都叫update_ota.img。

不过打包指导文件都是rk3308-package-file-ota。

我也不改这个机制了。直接在rk3308-package-file-ota这个文件上调整。

