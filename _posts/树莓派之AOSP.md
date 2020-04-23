---
title: 增量更新
date: 2018-06-18 22:17:08
tags:
	- Linux

---

1

https://github.com/tab-pi/platform_manifest

初始化repo。需要挂着梯子。

```
repo init -u https://github.com/tab-pi/platform_manifest -b nougat
```

同步

```
repo sync
```

然后编译kernel。

````
cd kernel/rpi
# 调用merge_config.sh，看名字，这个脚本是合并配置。
ARCH=arm scripts/kconfig/merge_config.sh arch/arm/configs/bcm2709_defconfig android/configs/android-base.cfg android/configs/android-recommended.cfg
# 进行编译
ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make zImage
ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make dtbs
````

安装mako模块。

```
sudo apt-get install python-mako
```

编译Android源代码

```
source build/envsetup.sh
lunch rpi-eng
make ramdisk systemimage
```

# 准备SD卡

SD卡的分区如下：

```
p1: 512MB，作为boot分区。fat32格式。
p2： 1024MB，作为system分区。ext4格式。
p3: 512MB。作为cache分区。ext4格式。
p4：剩余部分，作为data分区。ext4格式。
```

用dd命令把镜像烧录到SD卡的对应分区里。

```
cd out/target/product/rpi3
sudo dd if=system.img of=/dev/mmcblk0p2 bs=1M
```

拷贝kernel和ramdisk到boot分区。

```
sudo mount /dev/mmcblk0p1 /mymnt
cp device/brcm/rpi3/boot/* /mymnt
cp kernel/rpi/arch/arm/boot/zImage /mymnt
cp kernel/rpi/arch/arm/boot/bcm2710-rpi-3-b.dtb /mymnt
cp kernel/rpi/arch/arm/dts/overlays/vc4-kms-v3d.dtbo /mymnt/overlays
cp out/target/product/rpi3/ramdisk.img /mymnt
```

在config.txt里加上下面的语句，打开hdmi。

```
hdmi_group=2
hdmi_mode=85
```



写一个copy_boot.sh脚本。

```
#!/bin/sh

AOSP_DIR=/home/teddy/aosp-rpi3
MNT_DIR=/mymnt
FAT_DEV=/dev/sdc1

umount $MNT_DIR
mount $FAT_DEV $MNT_DIR
mkdir -p $MNT_DIR/overlays






sudo cp $AOSP_DIR/device/brcm/rpi3/boot/bootcode.bin      $MNT_DIR
sudo cp $AOSP_DIR/device/brcm/rpi3/boot/cmdline.txt      $MNT_DIR
sudo cp $AOSP_DIR/device/brcm/rpi3/boot/config.txt      $MNT_DIR
sudo cp $AOSP_DIR/device/brcm/rpi3/boot/fixup.dat      $MNT_DIR
sudo cp $AOSP_DIR/device/brcm/rpi3/boot/start.elf      $MNT_DIR


sudo cp $AOSP_DIR/kernel/rpi/arch/arm/boot/zImage    $MNT_DIR
sudo cp $AOSP_DIR/kernel/rpi/arch/arm/boot/dts/bcm2710-rpi-3-b.dtb   $MNT_DIR
sudo cp $AOSP_DIR/kernel/rpi/arch/arm/boot/dts/overlays/vc4-kms-v3d.dtbo  $MNT_DIR/overlays
sudo cp $AOSP_DIR/out/target/product/rpi3/ramdisk.img    $MNT_DIR

# umount $MNT_DIR

```



# 使用清华源

下载了很久都没有下载完成。

所以打算修改为清华源来进行同步。

只需要改这一行就可以了。

```
   <remote  name="aosp"
-           fetch="https://android.googlesource.com"
+           fetch="https://aosp.tuna.tsinghua.edu.cn"
```

可以在之前的同步到一半的基础上继续进行同步。

repo sync过程中，会出现的问题：

1、UnicodeDecodeError 问题

这个可以通过修改sitecustomize.py文件。这个文件在你的python库目录下。locate找一下就可以找打。

在最前面加上：

```
import sys
sys.setdefaultencoding("utf-8")
```

2、fatal: 过早的文件结束符（EOF）

这个网上说是网络问题。多次尝试就好了。

可以试一下这个命令：

```
repo sync -f -j4
```

用这个脚本反复下载，应该可以成功。

```
#!/bin/bash  
  
 echo ¨================start repo sync===============¨  
  
 repo sync -f -j4  
  
 while [ $? == 1 ]; do  
 echo ¨================sync failed, re-sync again=============¨  
 sleep 3  
 repo sync -f -j4  
 done  
```

使用清华源，还是有很多的错误。算了。我还是切换到谷歌源，慢慢下。



# android-rpi

对应url：https://github.com/android-rpi

来自于android-rpi这个项目下的project有3个：

```
hardware/rpi
external/mesa3d
external/drm_gralloc
```



# tab-pi

代码：https://github.com/tab-pi



来自这个项目的project有：

```
kernel/rpi 这个也是重点。
device/brcm/rpi3  这个是重点。
vendor/tab-pi 
frameworks/native
frameworks/base
hardware/broadcom/libbt
```



看看device/brcm/rpi3目录。这个是新增自己产品的方法的一个参考。

```
hlxiong@hlxiong-VirtualBox:~/work3/aosp-rpi3/device/brcm/rpi3$ tree -L 1
.
├── AndroidProducts.mk
├── audio_policy_configuration.xml
├── bluetooth
├── BoardConfig.mk
├── boot
├── firmware
├── fstab.rpi3
├── Generic.kl
├── init.rpi3.rc
├── init.usb.rc
├── overlay
├── README.md
├── rpi3_core_hardware.xml
├── rpi3.mk
├── sepolicy
├── system.prop
├── ueventd.rpi3.rc
└── vendorsetup.sh 这个下面新增了3个选项，在lunch的时候可以看到。add_lunch_combo rpi3-eng 这样。
```



# 运行测试

按照上面的说明，把4个分区都写入到SD卡。修改config.txt的参数。就可以正常启动了。

鼠标键盘都是正常的。

需要注意的是：

内核的是需要自己手动编译的，上面也有写了。



看看树莓派的kernel，相比于标准的kernel代码，改动了什么。

这个是自动挂载U盘。在fstab里。

```
/devices/platform/soc/*.usb/usb*     auto   auto      defaults   
```



这个下面就一个脚本，就是编译kernel的命令在里面，怎样才能调用到呢？

```
<project path="vendor/tab-pi" name="vendor_tab-pi" revision="nougat" remote="tab-pi"/>
```



framework native，也是用的tab-pi修改的。这个改了些什么？



参考资料

1、[ROM] [Testing] Tab-Pi | AOSP/Android TV for Raspberry Pi 3 android-7.1.2_r17

https://forum.xda-developers.com/raspberry-pi/development/rom-tab-pi-aosp-android-tv-raspberry-pi-t3593506