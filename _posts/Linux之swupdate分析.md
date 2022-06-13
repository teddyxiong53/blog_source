---
title: Linux之swupdate分析
date: 2022-03-29 14:19:25
tags:
	- Linux

---

--

主要两种机制：

AB系统

recovery系统



系统可以进入 “升级” 模式，

只需向引导加载程序发出必须启动升级软件的信号。 

具体方法可能有所不同，例如设置引导加载程序环境或使用和外部GPIO。



引导加载程序启动“SWUpdate”，

 引导SWUpdate内核**并将initrd映像作为根文件系统。**

 **因为它在RAM中运行，所以可以升级整个存储。**

 与双拷贝策略不同，系统**必须重新启动**以将其自身置于更新模式。

这个方案比起使用两个副本，占用的存储空间更少， 但是它不能保证在不再次更新软件的情况下进行回退。

 不过，至少它可以保证，当主应用不存在或损坏时， 以及当升级过程由于某种原因而中断时，系统自动进入升级模式。

![_images/single_copy_layout.png](https://zqb-all.github.io/swupdate/_images/single_copy_layout.png)



事实上，可以**将升级过程视为事务，**

 只有成功升级后，新软件才设置为“可引导”。 

考虑到这些因素，使用此策略进行升级是安全的:

 如果旧软件损坏或无法运行， 始终确保系统启动并准备好获得新软件。



使用U-Boot作为引导加载程序， 

SWUpdate能够管理U-Boot的环境设置变量， 

以指示事务的开始和结束，

以及包含有效的软件的存储区域。 

针对GRUB环境块修改和EFI Boot Guard的类似特性也已被引入。

SWUpdate主要以如下配置的方式使用。 

Yocto生成包含SWUpdate应用程序的initrd映像， 该映像在挂载根文件系统之后自动启动。



SWUpdate与引导加载程序一起工作，以识别失败的可能原因。 目前支持U-Boot、GRUB和EFI Boot Guard。



SWUpdate的工作流程是事务性的。

引导加载程序的环境变量“recovery_status” 被设置为向引导加载程序发出更新状态的信号。

 当然，还可以添加更多变量，用于微调和报告错误原因。

 recovery_status可以取值为“progress”，“failed”，或者它也可以被取消设置。

当SWUpdate启动时，它将recovery_status设置为“progress”。 更新成功完成后，变量将被删除。如果更新以错误结束， recovery_status的值为“failed”。



### 意外掉电

如果发生掉电，必须保证系统能够再次工作 —— 重新 启动SWUpdate或恢复软件的旧副本。

一般情况下，行为可以根据所选择的场景进行划分：

- 单拷贝：SWUpdate被中断，更新事务没有以成功结束。 引导加载程序能够再次启动SWUpdate，从而有可能再次更新软件。
- 双拷贝：SWUpdate没有在备份系统和当前系统之间做切换。 当前版本的软件，并没有被更新触及到，会再次启动。

为了完全安全，SWUpdate和引导加载程序需要交换一些信息。 

引导加载程序必须检测更新是否由于断电而中断， 并重新启动SWUpdate，直到更新成功。



SWUpdate支持U-Boot、GRUB和EFI Boot Guard引导加载程序。 

U-Boot和EFI Boot Guard**有用于保证掉电安全的环境变量**，

 SWUpdate能够读取和更改这些变量，

以此与引导加载程序通信。

 对于GRUB，则使用固定的1024字节环境变量块文件。 SWUpdate在开始更新系统时设置一个变量作为标志， 并在完成之后重置同一变量。引导加载程序可以读取此标志， 以检查在上次关机之前是否正在运行更新。



# amlogic

相关的配置项有：

```
BR2_PACKAGE_SWUPDATE=y
BR2_PACKAGE_SWUPDATE_CONFIG="package/swupdate/swupdate.config"
# BR2_PACKAGE_SWUPDATE_DOWNLOAD is not set
BR2_PACKAGE_SWUPDATE_INSTALL_WEBSITE=y
BR2_PACKAGE_SWUPDATE_AB_SUPPORT=""
```

测试方法：

有两种：

方法一：基于uboot

1、使用U盘的方式，先把software.swu文件放到U盘里。

2、进入到uboot命令行。

3、uboot下执行：run recovery_from_flash

方法二：基于网络方式

1、访问http://192.168.2.1 选择swupdate，进入到对应的界面，上传software.swu文件。

2、板端执行命令：

```
swupdate -l 6 -b "0 1 2 3 4 5" -k /etc/swupdate-public.pem -i /media/software.swu
```



/proc/inand 这个是amlogic自己定义的一个文件。里面放的是分区信息

https://github.com/endlessm/linux-meson/blob/master/drivers/mmc/card/emmc_partitions.c

```
/ # cat /proc/inand
dev:    size   erasesize  name
inand01:    400000     80000 "bootloader"
inand02:   4000000     80000 "reserved"
inand03:  46000000     80000 "cache"
inand04:    800000     80000 "env"
inand05:    800000     80000 "logo"
inand06:   2000000     80000 "recovery"
inand07:    800000     80000 "misc"
inand08:    800000     80000 "cri_data"
inand09:   1000000     80000 "param"
inand10:   4000000     80000 "boot"
inand11:   1000000     80000 "rsv"
inand12:   2000000     80000 "tee"
inand13:    800000     80000 "factory"
inand14:  1c000000     80000 "vendor"
inand15:    200000     80000 "vbmeta"
inand16:   8000000     80000 "odm"
```

```
if [ $1 == "start" ];then
  if [ -f "/proc/inand" ]; then
    swupdate --recovery -l 6 -k /etc/swupdate-public.pem -w "-r /var/www/swupdate/" > /tmp/swupdate.log &
  else
    swupdate --recovery -l 6 -k /etc/swupdate-public.pem -b "0 1 2 3 4" -w "-r /var/www/swupdate/" > /tmp/swupdate.log &
  fi
else
killall swupdate
fi
```

当前镜像在150M左右。而software.swu大小在130M左右。

software.swu是怎么生成的？



在package/swupdate目录下，amlogic的patch，还是做了不小的修改。

```
1, Support AML Uboot env
2, Support ab update
3, Support EXT4
4, Support Recovery download
5, Support bootloader offset
```



私钥放在这里./buildroot/board/amlogic/common/ota/swu/swupdate-priv.pem

分析./buildroot/board/amlogic/common/ota/swu/目录下的脚本。

ota_package_create.sh脚本。

```
OTA_SRC_PATH=../build/buildroot-fs/cpio/target_ota
source ota-package-filelist

签名
openssl dgst -sha256 -sign swupdate-priv.pem sw-description > sw-description.sig
打包
for i in $FILES;do
	echo $i;done | cpio -ov -H crc >  software.swu
echo software.swu  | cpio -ov -H crc >  ${PRODUCT_NAME}_${CONTAINER_VER}.swu
```

这个就是会被打包到ota 的software.swu里的文件。

build/buildroot-fs这个目录下的文件是怎么生成的？

现在target_recovery和target_ota目录下，都是121M的文件。太多了。

ota-package-filelist 这个文件在哪里？

在这里：./output/a5_av400_a6432_release/images/ota-package-filelist

是生成的。

里面就3行：

```
 # ota package file list for emmc
 HASH_FILES="u-boot.bin dtb.img boot.img rootfs.ext2.img2simg update.sh"
 FILES="sw-description sw-description.sig u-boot.bin dtb.img boot.img rootfs.ext2.img2simg update.sh"
```

在images目录下，有生成这样的一些压缩包：target_ota_2203280716.zip

里面的内容是：

![image-20220330103315081](../images/random_name/image-20220330103315081.png)



```
# blacklist.txt, a list of blacklists to call before generating the filesystem rootfs.tar
# If you do not want some bin to be packaged into rootfs, Please write the name of the bin below.
```



boot.img是这样生成的：

mk_bootimg.sh脚本生成

```
./buildroot/linux/mkbootimg \
--kernel build/linux-amlogic-5.4-dev/arch/arm64/boot/Image.gz \
--base 0x0 \
--kernel_offset 0x1080000 \
--cmdline "root=/dev/system rootfstype=ext4 init=/sbin/init" \
--ramdisk images/rootfs.cpio.gz \
--second images/a5_a113x2_av400_1g.dtb \
--output images/boot.img
```

mkbootimg 这个二进制是我们加的。这个是从安卓那边拿过来的工具。

boot.img也是安卓的一个标准做法。我们是拿到Linux上来用了。



看看之前S420的target_ota和target_recovery有多大。

也是一样的大。都是100多M。

这个合理吗？

platform.conf里的内容：

```
Platform:0x0812
soctype:A5
```

从这个目录./buildroot/board/amlogic/common/upgrade/upgrade-a5拷贝过来的。

分析一下这个目录下的文件。

```
aml_sdc_burn.ini  这个就是我从A1的拷贝过来了，没有改动。
aml_upgrade_package_ab.conf
aml_upgrade_package.conf
	头部的注释写着：
	#This file define how pack aml_upgrade_package image
aml_upgrade_package_emmc_ab.conf
aml_upgrade_package_emmc.conf
aml_upgrade_package_emmc_enc.conf
aml_upgrade_package_enc.conf
aml-user-key.sig 这个就是我从A1的拷贝过来了，没有改动。
keys.conf  这个就是我从A1的拷贝过来了，没有改动。
platform.conf  这个后面SamWu提交了一下。
usb_flow.aml  这个后面SamWu提交了一下。
```

分析一下buildroot/board/amlogic/common/ota/ota-a5目录

```
ota-package-filelist-emmc
	这个就是会被拷贝生成ota-package-filelist
ota-package-filelist-emmc-enc
ota-package-filelist-nand
ota-package-filelist-nand-enc
ramdisk
	目录。
ramfslist-recovery-need
	这个描述了recovery需要的内容。
sw-description-emmc
sw-description-emmc-enc
sw-description-emmc-increment
sw-description-emmc-increment-enc
sw-description-nand
sw-description-nand-ab
sw-description-nand-enc
sw-description-nand-increment
sw-description-nand-increment-enc
```

ramdisk目录里

```
./etc
./etc/mdev.conf
./etc/init.d
./etc/init.d/S01swupdate
./etc/init.d/rcS
./etc/hotplug
./etc/hotplug/remove.sh
./etc/hotplug/insert.sh
./init
```



需要在看一下buildroot/fs目录。

看看buildroot/fs/common.mk

```
FS_DIR = $(BUILD_DIR)/buildroot-fs
所以build目录下那个buildroot-fs是这里生成的。
BR2_ROOTFS_DEVICE_TABLE="system/device_table.txt"
这个是buildroot/system/device_table.txt文件。
整理生成到full_devices_table.txt文件里。
```



BR2_REPRODUCIBLE

```
BR2_ROOTFS_COMMON_OVERLAY=""
BR2_ROOTFS_UPGRADE_DIR="board/amlogic/common/upgrade/upgrade-a5/"
BR2_RECOVERY_OTA_DIR="board/amlogic/common/ota/ota-a5/"
BR2_RECOVERY_OTA_RAMDISK_DIR=""
BR2_ROOTFS_UPGRADE_DIR_OVERLAY=""
BR2_ROOTFS_OVERLAY="board/amlogic/mesona5_av400/rootfs/"
```

生成在这个目录下：

./output/a5_av400_a6432_release/host/bin/ramfslist-recovery

列出了recovery需要的文件。

recovery.img 当前是14M左右。

recovery.img里被打包进去了哪些东西？包括了kernel吗？

是这里：

```
./fs/cpio/cpio.mk:151:# linux/mkbootimg --kernel $(LINUX_IMAGE_PATH) --base 0x0 --kernel_offset $(LINUX_KERNEL_BOOTIMAGE_OFFSET) --cmdline "$(KERNEL_BOOTARGS)" --ramdisk  $(BINARIES_DIR)/recovery.cpio.gz --second $(BINARIES_DIR)/dtb.img --output $(BINARIES_DIR)/recovery.img
```

可以看到了包括了kernel、dtb、一个小的rootfs。

看recovery.cpio.gz里包含了哪些内容。

BR2_TARGET_ROOTFS_INITRAMFS_LIST

BR2_TARGET_RECOVERY_INITRAMFS_LIST

```
BR2_TARGET_ROOTFS_INITRAMFS_LIST="board/amlogic/mesona5_av400/initramfs/ramfslist-32-ext2"
 BR2_TARGET_RECOVERY_INITRAMFS_LIST=""
```

所以，recovery没有initramfs。



我们当前的initramfs。

有会怎么样？没有会怎么样？

![image-20220330133352393](../images/random_name/image-20220330133352393.png)

这个就是initramfs的内容。

在/proc/cmdline里，看到

```
rootfstype=ramfs
```

所以这个是去找initramfs。

但是同时还有：

```
root=/dev/system
rootfstype=ext4
init=/sbin/init
```

有怎么理解呢？

而且可能是被后面的覆盖了。

把flash里的分区挂载到/mnt先。

```
mount "${root}" /mnt
```

最后切换root

```
exec switch_root -c /dev/console /mnt "${init}"
```



这个依赖关系，linux-rebuild-with-initramfs在哪里定义，做了什么？

```
rootfs-initramfs: linux-rebuild-with-initramfs
```

是在linux.mk里定义的。

```
.PHONY: linux-rebuild-with-initramfs
linux-rebuild-with-initramfs: $(LINUX_DIR)/.stamp_target_installed
linux-rebuild-with-initramfs: $(LINUX_DIR)/.stamp_images_installed
linux-rebuild-with-initramfs: rootfs-cpio
linux-rebuild-with-initramfs: $(BINARIES_DIR)/$(ROOTFS_CPIO)
linux-rebuild-with-initramfs:
	@$(call MESSAGE,"Rebuilding kernel with initramfs")
	# Build the kernel.
```



通过tab补全make rootfs- 查看到

```
rootfs-cpio             
rootfs-cpio-show-depends
rootfs-cpio-show-info   

rootfs-ext2               
rootfs-ext2-show-depends  
rootfs-ext2-show-info     

 rootfs-initramfs              
 rootfs-initramfs-show-depends 
```

分析make rootfs-cpio的输出日志打印

使用安卓镜像格式，是这个配置项控制的。

```
ifeq ($(BR2_LINUX_KERNEL_ANDROID_FORMAT),y)
```

在这里配置的

```
./a5_base.config:20:BR2_LINUX_KERNEL_ANDROID_FORMAT=y
```



```
host-skeleton
这个的用途是什么？
skeleton

对应的是package/skeleton
$(eval $(virtual-package))
$(eval $(host-generic-package))
没啥用。
在build目录下生成了空的目录（只有几个隐藏的flag文件）

```



```
aml-bootloader-message-0.1 
aml-ubootenv-0.1 
aml-usb-config 
```



```
int get_store_device() {
    int ret = 0;
    ret = access("/proc/inand", F_OK);
    if (ret == 0 ) {
        printf("emmc device!\n");
        return 0;
    } else {
        printf("nand device!\n");
        return -1;
    }
}
```



/dev/misc 这个设备的作用。

往里面写信息，跟bootloader进行升级相关的通信。

写入的信息，就是bootloader_message结构体，里面包含了升级包信息。

set_recovery_otapath这个函数，有2个文件调用了

```
Binary file ./usr/bin/swupdate matches
Binary file ./usr/bin/urlmisc matches
```

urlmisc作用是什么？从代码看，好像是写入升级包信息，估计是手动进行升级测试用的。

```
void usage() {
        printf("eg:urlmisc write http://xx.28.xx.53:8080/otaupdate/swupdate/software.swu\n");
        printf("     urlmisc read\n");
        printf("     urlmisc clean\n");
        printf("     urlmisc local\n");
}
```



uboot-env的package，是在kernel下对uboot的环境变量进行读写操作。

对应的/dev/env 这个设备节点。

这些设备节点的名字是如何确定的？

是不是设备树里配置就可以达到这个效果？

设备树里没有名为env的分区，是在rsv分区里。另外有驱动。可以在kernel/drivers/amlogic下面grep找到相关代码。



使用结构化语言描述镜像，这个由libconfig库作为缺省的解析，像使用json描述

网络安装可以使用一个嵌入式的Web服务器（选择mongoose服务器，基于Lua license版本），也可以选择不同的Web服务器



单个升级包镜像

主要的做法是，厂商提供一个大的镜像文件，

所有待更新的分区镜像与软件描述文件sw-description都被打包在一起（选择cpio，简单且支持流），

sw-description包含每个单个镜像的元数据。

sw-description的格式可以定制，

swupdate可以配置使用内部的解析器（基于libconfig），

或者使用外部的lua解析器。



既然可以使用外部的解析器，而非使用默认的解析器（libconfig），

同样升级镜像的类型和安装方式也可以定制，

解析器无非就是找出哪个镜像需要安装到哪里去，

swupdate使用叫做handler的处理程序去安装单个镜像，

处理安装镜像的handlers包含ubi volume，sd card，cfi flash等等，

如果有特殊的镜像需要安装，很容易添加一个自定义的hander处理程序。



原生的swupdate版本已经支持raw ubifs的升级，对于ext4的镜像不支持升级，我们公版最新版本已经支持ext4镜像升级。



我们可以通过make swupdate-menuconfig来对swupdate进行配置，具体每个配置项可详细了解。



本地升级：

进入recovery之后，会自动挂载U盘设备，

在U盘的根目录寻找名字为software.swu的升级包，

如果升级包存在，则进行本地升级，否则提示，没有找到升级包的相关信息。

网络升级：

我们可以连接ap，访问设备的地址（eg：192.168.2.1），

登陆设备的管理页面，选择swupdate的选项，

选择升级包（aml-software_1.0.swu）升级，

**选择了升级包后，swupdate升级模块会把升级包下载到data分区存放（保存名为software.swu），**

然后重启进入recovery从data分区读取升级包升级。

**注意：由于网络升级需要把升级包存放到data分区，然后从data分区获取升级包升级，那么前提条件是data分区的可用大小，必须大于升级包的大小，否则data分区无法保存完整的升级包大小。**



我们通过make之后会在output下面生成我们需要的镜像，以s400 debug版本为例：

  recovery.img  基于swupdate的升级模块。

  aml-software-1.0.swu： 通过web页面升级的升级包。

  software.swu：本地升级的升级包。

这三个文件都会生成在路径：output\mesonaxg_s400_debug\images

software.swu与aml-software-1.0.swu分别是本地升级及web网络升级的升级包，其中aml-software-1.0.swu比software.swu**多了一层cpio的打包头信息**，不可混淆。



我们的升级过程采用一对密钥进行签名校验，密钥路径：

公钥：buildroot\board\amlogic\common\rootfs\rootfs-xxxx\etc\swupdate-public.pem

私钥：buildroot\board\amlogic\common\ota\swu\swupdate-priv.pem

 公钥打包到recovery系统路径/etc/swupdate-public.pem，

私钥我们用来对sw-description生成签名sw-description.sig, 

我们在读取升级包software.swu之后，

读取/etc/swupdate-public.pem公钥来验证sw-description签名是否正确。

 升级包中每个镜像对应的sha256值保存在sw-description中，

其中的镜像如果有任何改变，则校验值将发生变化，校验不过，

如果sw-description有修改，则对应的sw-description.sig信息校验时，无法正常校验通过。

从而保证升级包的完整及正确性。



aml_upgrade_package_emmc.conf

这个还是看懂了。打包生成aml_upgrade_package.img

u-boot.bin.signed里就包含了多个bootloader的。

```
file="boot.img"             main_type="PARTITION"       sub_type="boot"
file="recovery.img"         main_type="PARTITION"       sub_type="recovery"
file="rootfs.ext2.img2simg"           main_type="PARTITION"       sub_type="system"
file="u-boot.bin.signed"           main_type="PARTITION"       sub_type="bootloader"
file="dtb.img"              main_type="PARTITION"       sub_type="_aml_dtb"
```

ota-a5里有个ramdisk目录。

这个是recovery打包进kernel的initramfs的内容。



ramfslist-recovery-need

这个在哪里被使用？

```
./fs/cpio/cpio.mk:86:   cat $(RECOVERY_OTA_DIR)/ramfslist-recovery-need >> $(HOST_DIR)/bin/ramfslist-recovery
```



重点看看这个脚本。

ota_package_create.sh

调用这个脚本的只有：

```
./fs/ubi/ubi.mk:76:     $(BINARIES_DIR)/ota_package_create.sh
./fs/ubi/ubi.mk:84:     $(BINARIES_DIR)/ota_package_create.sh
./fs/ext2/ext2.mk:98:   $(BINARIES_DIR)/ota_package_create.sh
```

看看ext2.mk的内容。

BR2_PACKAGE_AML_VENDOR_PARTITION

这个当前没有配置。

uboot2015的调用了aml_upgrade_pkg_gen.sh

非uboot2015的，调用了aml_image_v2_packer_new

```
$(HOST_DIR)/bin/aml_image_v2_packer_new -r $(BINARIES_DIR)/aml_upgrade_package.conf $(BINARIES_DIR)/ $(BINARIES_DIR)/aml_upgrade_package.img
```

BR2_TARGET_UBOOT_ENCRYPTION

这个uboot加密，当前没有使能。

```
ifeq ($(BR2_TARGET_UBOOT_ENCRYPTION),y)
	RECOVERY_ENC_FLAG="-enc"
endif
```

生成software.swu的代码

```
define ROOTFS-OTA-SWU-PACK-EXT4FS
	$(INSTALL) -m 0755 $(RECOVERY_OTA_DIR)/../swu/* $(BINARIES_DIR)
	$(INSTALL) -m 0644 $(RECOVERY_OTA_DIR)/sw-description-emmc$(RECOVERY_ENC_FLAG) $(BINARIES_DIR)/sw-description
	$(INSTALL) -m 0644 $(RECOVERY_OTA_DIR)/sw-description-emmc-increment$(RECOVERY_ENC_FLAG) $(BINARIES_DIR)/sw-description-increment
	$(INSTALL) -m 0644 $(RECOVERY_OTA_DIR)/ota-package-filelist-emmc$(RECOVERY_ENC_FLAG) $(BINARIES_DIR)/ota-package-filelist
	$(BINARIES_DIR)/ota_package_create.sh
endef
```

看看这3个文件：

sw-description-emmc

sw-description-emmc-increment

ota-package-filelist-emmc

这3个文件都需要改一下。

看看images\sw-description文件里。

很明显，uboot的sha256值没有正确生成。

```
{
			filename = "boot.img";
			sha256 = "91f841028f9288b9df834501c8a189b5aaecbe4c6083965638d3616467043cce"
			device = "/dev/boot";
		},
		{
			filename = "u-boot.bin";
			sha256 = ""
			device = "/dev/bootloader";
		}
```

HASH_FILES是表示需要计算hash值的文件。其余的文件不用计算。



参考资料

https://confluence.amlogic.com/display/SW/SWUpdate

这个很详细了。需要反复看懂。

https://wiki-china.amlogic.com/index.php?title=%e5%86%85%e9%83%a8%e4%ba%ba%e5%91%98%e5%8f%82%e8%80%83%e8%b5%84%e6%96%99/AE_internal-Q%26A/Common/Buildroot_recovery_%e5%8d%87%e7%ba%a7



# sw-description



参考资料

这篇文章很全面了。

https://blog.csdn.net/weixin_30312563/article/details/99878653



# 增量升级

目前增量升级依赖于system挂载为ro只读模式，否则差分升级具有局限性，且具有不安全性，待系统分区修改挂载为ro之后，再提交相关差分升级功能。



# 参考资料

1、

https://zqb-all.github.io/swupdate/overview.html

2、

https://blog.csdn.net/luzhenrong45/article/details/62042400