---
title: 树莓派3b安装Android系统
date: 2020-03-18 09:50:11
tags:
	- 树莓派
---

1

最近看metasploit对Android的渗透方法，发现Android远比想象的脆弱。

使用meterpreter控制手机的时候，只是会弹出权限请求。看不出其他的异常。只要把meterpreter跟正常的apk绑定起来，就很难看出异常了。

所以我觉得有必要对Android系统进行一些深入的认识。

用手机来做的话，现在一个是没有空余好用的手机，二个是现在手机root都没有那么容易了。

而且手机不方便看到底层的调试信息。

所以我就想到用树莓派来刷Android来进行研究。

网上搜索了一些，很容易就找到一些成功的例子。

我就参考这个来做。刷入镜像启动都没有问题。启动正常。

https://konstakang.com/devices/rpi3/LineageOS16.0/

lineageos是不带GMS的社区开源版本。

压缩包400多M，解压后4G。

有线、无线、鼠标、键盘都工作正常。

当前这个镜像支持的：

```
1、音频正常。包括hdmi、3.5mm jack、蓝牙耳机，usb麦克风。
2、蓝牙。
3、相机。
4、以太网。
5、hdmi显示。
6、串口。
7、触摸屏。
8、usb设备。
9、wifi。
```

对应的内核代码：

https://github.com/lineage-rpi/android_kernel_brcm_rpi/tree/lineage-16.0



Q：怎么打开开发者模式？

A：进入设置，关于，连续点击build number好几次。就打开了。

Q：没有root权限

A：在开发者选项里，选择root enable。



其实我现在需要的是在串口console切换为root身份进行操作。

应该怎么做呢？



```
255|console:/system/xbin $ df -h
Filesystem           Size  Used Avail Use% Mounted on
tmpfs                370M  320K  370M   1% /dev
tmpfs                370M     0  370M   0% /mnt
/dev/block/mmcblk0p1 126M   38M   88M  31% /boot
/dev/block/mmcblk0p2 0.9G  756M  236M  77% /system
/dev/block/mmcblk0p3 248M   20M  223M   9% /vendor
/dev/block/mmcblk0p4 2.5G   77M  2.2G   4% /data
/data/media          2.5G   77M  2.2G   4% /storage/emulated
```

可以看到sd卡被分了4个分区：

1、boot分区。

2、system分区。

3、vendor分区。

4、data分区，这个分区，2个路径都可以访问，一个/data，一个/storage/emulated。

但是data分区进去ls都没有权限。



在串口console，怎么切换到root身份呢？当前设备已经打开root了。

```
# 执行su就够了，我以为会要折腾很久才能可以的。
$ su
```

```
console:/etc/init.d $ su
:/ # 
:/ # whoami                                                                    
root
```

当前内存虽然不大，但是因为也没有打开什么应用。所以内存还有剩余。

```
:/data # free -m
                total        used        free      shared     buffers
Mem:              740         488         252           0           3
-/+ buffers/cache:            485         255
Swap:             383          56         327
```

挂载信息。

```
/dev/block/mmcblk0p1 on /boot type vfat (ro,relatime,fmask=0000,dmask=0000,allow_utime=0022,codepage=437,iocharset=ascii,shortname=mixed,errors=remount-ro)
/dev/block/mmcblk0p2 on /system type ext4 (ro,seclabel,relatime)
/dev/block/mmcblk0p3 on /vendor type ext4 (ro,seclabel,relatime)
/dev/block/mmcblk0p4 on /data type ext4 (rw,seclabel,nosuid,nodev,noatime,errors=panic)
```

可以看到只要分区4是可写的。

```
/data/media on /mnt/runtime/default/emulated type sdcardfs (rw,
/data/media on /storage/emulated type sdcardfs (rw,nosuid,nodev
/data/media on /mnt/runtime/read/emulated type sdcardfs (rw,nos
/data/media on /mnt/runtime/write/emulated type sdcardfs (rw,no
```

可以看到Android里用的是toybox，而不是busybox。

```
cat -> toybox
```

Android之前还用过一个叫toolbox的。现在这个toolbox已经停止维护了。

根目录下有这些文件和目录。

```
acct/  
bin/  toyxbox的各种ls、cat工具。
boot/  boot分区。kernel在这里。
bugreports 
cache/  
charger 这个是可执行程序。
config/ 
d/  这个实际上是设备树。
data/  
default.prop 文本文档，一些属性配置。
dev/ 
etc/
fstab.rpi3 一个文件挂载表。
init  
init.environ.rc
init.rc
init.rpi3.rc
init.usb.configfs.rc
init.usb.rc
init.zygote32.rc
mnt/
odm/
oem/
plat_file_contexts
plat_hwservice_contexts
plat_property_contexts
plat_seapp_contexts
plat_service_contexts
proc/
product/
res/
root/
sbin/
sdcard/
sepolicy
storage/
sys/
system/
ueventd.rc
ueventd.rpi3.rc
vendor/
vendor_file_contexts
vendor_hwservice_contexts
vendor_property_contexts
vendor_seapp_contexts
vendor_service_contexts
vndservice_contexts
```









参考资料

1、LineageOS 16.0 (Android 9)

https://konstakang.com/devices/rpi3/LineageOS16.0/

2、How can I execute command in the terminal as root?

https://android.stackexchange.com/questions/4021/how-can-i-execute-command-in-the-terminal-as-root

3、Android的toolbox及busybox,toybox

https://blog.csdn.net/ly890700/article/details/72615465