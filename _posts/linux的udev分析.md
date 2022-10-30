---
title: linux的udev分析
date: 2016-12-10 21:58:22
tags:
	- linux驱动
	- udev
---
linux下的设备文件处理这一块，在多年的发展过程中，经历了几次策略的改变。

在早期，设备文件仅仅是一些带有适当属性集的普通文件，它由mknod命令创建，文件存放在/dev目录下。

后来，从内核2.3.46版本开始，采用了devfs，一个基于内核的动态设备文件系统。

但是devfs有比较严重的限制，于是，从内核2.6.13版本起，devfs又被移除了。替换为现在要说的udev。

devfs的缺点有很多，主要有这些：

* 不确定的设备映射。你的设备名字跟你插入的顺序有关。
* 主设备号和从设备号不够用，它们的数值都是最大为255 。
* 内核内存使用，devfs会消耗大量的内核内存。
相比于前辈们，udev很好地解决了设备的热拔插问题，还有解决了devfs的设备号短缺的问题，这一点对于有上千个硬盘的系统非常关键。

udev的配置文件是`/etc/udev/udev.conf`。
在树莓派上，该文件的内容如下所示，是空的。

```
# see udev(7) for details
#
# udevd is started in the initramfs, so when this file is modified the
# initramfs should be rebuilt.

#udev_log="info"
                                                                         
```
我的当前的树莓派插着一个U盘，被格式化为2个分区。查看一下sda1的信息。
```
pi@raspberrypi:/sys/block/sda/sda1 $ udevadm info /sys/block/sda/sda1 
P: /block/sda/sda1
N: sda1
S: disk/by-id/usb-Kingston_DataTraveler_G3_001CC07CEB39FBB1C91A24D0-0:0-part1
S: disk/by-label/BOOT
S: disk/by-path/platform-3f980000.usb-usb-0:1.5:1.0-scsi-0:0:0:0-part1
S: disk/by-uuid/47CE-67C0
E: DEVLINKS=/dev/disk/by-id/usb-Kingston_DataTraveler_G3_001CC07CEB39FBB1C91A24D0-0:0-part1 /dev/disk/by-label/BOOT /dev/disk/by-path/platform-3f980000.usb-usb-0:1.5:1.0-scsi-0:0:0:0-part1 /dev/disk/by-uuid/47CE-67C0
E: DEVNAME=/dev/sda1
E: DEVPATH=/block/sda/sda1
E: DEVTYPE=partition
E: ID_BUS=usb
E: ID_FS_LABEL=BOOT
E: ID_FS_LABEL_ENC=BOOT
E: ID_FS_TYPE=vfat
E: ID_FS_USAGE=filesystem
E: ID_FS_UUID=47CE-67C0
E: ID_FS_UUID_ENC=47CE-67C0
E: ID_FS_VERSION=FAT32
E: ID_INSTANCE=0:0
E: ID_MODEL=DataTraveler_G3
E: ID_MODEL_ENC=DataTraveler\x20G3\x20
E: ID_MODEL_ID=1643
E: ID_PART_ENTRY_DISK=8:0
E: ID_PART_ENTRY_NUMBER=1
E: ID_PART_ENTRY_OFFSET=2048
E: ID_PART_ENTRY_SCHEME=dos
E: ID_PART_ENTRY_SIZE=192512
E: ID_PART_ENTRY_TYPE=0xc
E: ID_PART_ENTRY_UUID=885f1eb8-01
E: ID_PART_TABLE_TYPE=dos
E: ID_PART_TABLE_UUID=885f1eb8
E: ID_PATH=platform-3f980000.usb-usb-0:1.5:1.0-scsi-0:0:0:0
E: ID_PATH_TAG=platform-3f980000_usb-usb-0_1_5_1_0-scsi-0_0_0_0
E: ID_REVISION=1.00
E: ID_SERIAL=Kingston_DataTraveler_G3_001CC07CEB39FBB1C91A24D0-0:0
E: ID_SERIAL_SHORT=001CC07CEB39FBB1C91A24D0
E: ID_TYPE=disk
E: ID_USB_DRIVER=usb-storage
E: ID_USB_INTERFACES=:080650:
E: ID_USB_INTERFACE_NUM=00
E: ID_VENDOR=Kingston
E: ID_VENDOR_ENC=Kingston
E: ID_VENDOR_ID=0951
E: MAJOR=8
E: MINOR=1
E: SUBSYSTEM=block
E: TAGS=:systemd:
E: USEC_INITIALIZED=76296
```

udev的命名规则保存在`/etc/udev/rules.d`目录下。目录下的脚本名字是用数字来编号。从数字小的开始执行，**一旦发现匹配的规则，则停止执行返回。**
树莓派的Raspbian系统的该目录下，就一个`99-com.rules`文件。内容如下：

```
SUBSYSTEM=="input", GROUP="input", MODE="0660"
SUBSYSTEM=="i2c-dev", GROUP="i2c", MODE="0660"
SUBSYSTEM=="spidev", GROUP="spi", MODE="0660"
SUBSYSTEM=="bcm2835-gpiomem", GROUP="gpio", MODE="0660"

SUBSYSTEM=="gpio*", PROGRAM="/bin/sh -c '\
    chown -R root:gpio /sys/class/gpio && chmod -R 770 /sys/class/gpio;\
    chown -R root:gpio /sys/devices/virtual/gpio && chmod -R 770 /sys/devices/virtual/gpio;\
    chown -R root:gpio /sys$devpath && chmod -R 770 /sys$devpath\
'"

KERNEL=="ttyAMA[01]", PROGRAM="/bin/sh -c '\
    ALIASES=/proc/device-tree/aliases; \
    if cmp -s $ALIASES/uart0 $ALIASES/serial0; then \
        echo 0;\
    elif cmp -s $ALIASES/uart0 $ALIASES/serial1; then \
        echo 1; \
    else \
        exit 1; \
    fi\
'", SYMLINK+="serial%c"

KERNEL=="ttyS0", PROGRAM="/bin/sh -c '\
    ALIASES=/proc/device-tree/aliases; \
    if cmp -s $ALIASES/uart1 $ALIASES/serial0; then \
        echo 0; \
    elif cmp -s $ALIASES/uart1 $ALIASES/serial1; then \
        echo 1; \
    else \
        exit 1; \
    fi \
'", SYMLINK+="serial%c"
```

mdev是udev在busybox里的精简版本。



buildroot里udev

在/etc/init.d/S10udev里进行的。往proc/sys/kernel/hotplug   写入了0，是说明不支持热插拔吗？

```
 printf "Populating %s using udev: " "${udev_root:-/dev}"      
 printf '\000\000\000\000' > /proc/sys/kernel/hotplug          
 $UDEV_BIN -d || { echo "FAIL"; exit 1; }                      
 udevadm trigger --type=subsystems --action=add                
 udevadm trigger --type=devices --action=add                   
 udevadm settle --timeout=30 || echo "udevadm settle failed"   
 echo "done"                                                   
```

对应的配置文件是在/etc/udev目录下。

```
/etc/udev # ls                   
hwdb.d     这个下面有很多文件。
rules.d   空的
udev.conf  这个是空的
```



udev是一个通用的内核设备管理器。它以守护进程的方式运行于Linux系统，并监听在新设备初始化或设备从系统中移除时，内核（通过netlink socket）所发出的uevent。

# udev系统架构：

udev系统可以分为三个部分：

- libudev函数库，可以用来获取设备的信息。
- udevd守护进程，处于用户空间，用于管理虚拟/dev
- 管理命令udevadm，用来诊断出错情况。



# udevadm命令



```
/etc # udevadm info --query=all --name=rk_led_ctrl       
P: /devices/platform/pwm_leds@0/misc/rk_led_ctrl         
N: rk_led_ctrl                                           
E: DEVNAME=/dev/rk_led_ctrl                              
E: DEVPATH=/devices/platform/pwm_leds@0/misc/rk_led_ctrl 
E: MAJOR=10                                              
E: MINOR=0                                               
E: SUBSYSTEM=misc                                        
```



使用udev实现USB，SD卡设备的重命名、自动挂载、自动卸载。



自动创建设备节点，靠class机制就可以做到了。

我们在刚开始写[Linux](http://lib.csdn.net/base/linux)设备驱动程序的时候，很多时候都是利用mknod命令手动创建设备节点，实际上Linux内核为我们提供了一组函数，可以用来在模块加载的时候自动在/dev目录下创建相应设备节点，并在卸载模块时删除该节点，当然前提条件是用户空间移植了udev。



内核中定义了struct class结构体，顾名思义，一个struct class结构体类型变量对应一个类，内核同时提供了class_create(…)函数，可以用它来创建一个类，这个类存放于sysfs下面，一旦创建好了这个类，再调用device_create(…)函数来在/dev目录下创建相应的设备节点。**这样，加载模块的时候，用户空间中的udev会自动响应device_create(…)函数，去/sysfs下寻找对应的类从而创建设备节点。**



# buildroot里的udevd

是在eudev目录下，而不是udevd目录下。



# 参考资料

1、udev udevadm介绍及linux设备重命名和自动挂载应用实例分析

https://blog.csdn.net/li_wen01/article/details/89435306

2、linux下自动创建设备文件节点---class

https://www.cnblogs.com/Ph-one/p/6720087.html