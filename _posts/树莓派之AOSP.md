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
cd out/target/product/rpi
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



参考资料

1、

